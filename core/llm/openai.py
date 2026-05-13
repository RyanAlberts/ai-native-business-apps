# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""OpenAI adapter — runs the tool loop manually against chat.completions."""
from __future__ import annotations

import inspect
import os

from .base import LLMClient, LLMConfig, Tool, parse_tool_args


class OpenAIClient(LLMClient):
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        try:
            from openai import AsyncOpenAI
        except ImportError as e:
            raise RuntimeError(
                "openai package not installed. Install with: pip install openai"
            ) from e
        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY not set.")
        self._client = AsyncOpenAI()

    async def complete(
        self,
        system_prompt: str,
        user_message: str,
        tools: list[Tool] | None = None,
    ) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
        oai_tools = [_to_openai_tool(t) for t in (tools or [])] or None
        tool_map = {t.name: t for t in (tools or [])}

        for _ in range(self.config.extra.get("max_turns", 12)):
            resp = await self._client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                tools=oai_tools,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )
            msg = resp.choices[0].message
            if not msg.tool_calls:
                return msg.content or ""
            messages.append(
                {
                    "role": "assistant",
                    "content": msg.content or "",
                    "tool_calls": [tc.model_dump() for tc in msg.tool_calls],
                }
            )
            for tc in msg.tool_calls:
                tool = tool_map.get(tc.function.name)
                if not tool:
                    result = f"unknown tool: {tc.function.name}"
                else:
                    args = parse_tool_args(tc.function.arguments, tc.function.name)
                    if isinstance(args, str):
                        result = args
                    else:
                        raw = tool.handler(args)
                        if inspect.isawaitable(raw):
                            raw = await raw
                        result = str(raw)
                messages.append(
                    {"role": "tool", "tool_call_id": tc.id, "content": result}
                )
        return "Tool loop exceeded max_turns without final response."


def _to_openai_tool(t: Tool) -> dict:
    return {
        "type": "function",
        "function": {
            "name": t.name,
            "description": t.description,
            "parameters": t.input_schema,
        },
    }
