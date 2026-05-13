# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Gemini adapter — runs the tool loop manually against the Generative AI SDK."""
from __future__ import annotations

import inspect
import os

from .base import LLMClient, LLMConfig, Tool, parse_tool_args


class GeminiClient(LLMClient):
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        try:
            from google import genai
        except ImportError as e:
            raise RuntimeError(
                "google-genai package not installed. "
                "Install with: pip install google-genai"
            ) from e
        if not os.environ.get("GOOGLE_API_KEY"):
            raise RuntimeError("GOOGLE_API_KEY not set.")
        self._client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

    async def complete(
        self,
        system_prompt: str,
        user_message: str,
        tools: list[Tool] | None = None,
    ) -> str:
        from google.genai import types as gtypes

        gemini_tools = (
            [
                gtypes.Tool(
                    function_declarations=[
                        gtypes.FunctionDeclaration(
                            name=t.name,
                            description=t.description,
                            parameters=t.input_schema,
                        )
                        for t in tools
                    ]
                )
            ]
            if tools
            else None
        )
        tool_map = {t.name: t for t in (tools or [])}

        chat = self._client.aio.chats.create(
            model=self.config.model,
            config=gtypes.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=gemini_tools,
                temperature=self.config.temperature,
                max_output_tokens=self.config.max_tokens,
            ),
        )
        next_input = user_message

        for _ in range(self.config.extra.get("max_turns", 12)):
            resp = await chat.send_message(next_input)
            calls = getattr(resp, "function_calls", None) or []
            if not calls:
                return resp.text or ""
            tool_responses = []
            for call in calls:
                tool = tool_map.get(call.name)
                if not tool:
                    out = f"unknown tool: {call.name}"
                else:
                    args = parse_tool_args(call.args, call.name)
                    if isinstance(args, str):
                        out = args
                    else:
                        raw = tool.handler(args)
                        if inspect.isawaitable(raw):
                            raw = await raw
                        out = raw
                tool_responses.append(
                    gtypes.Part.from_function_response(
                        name=call.name,
                        response={"result": out if isinstance(out, (dict, list, str)) else str(out)},
                    )
                )
            next_input = tool_responses
        return "Tool loop exceeded max_turns without final response."
