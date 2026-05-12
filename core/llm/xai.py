# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""xAI adapter — uses the OpenAI SDK pointed at api.x.ai (Grok is OpenAI-compatible)."""
from __future__ import annotations

import inspect
import json
import os

from .base import LLMClient, LLMConfig, Tool


class XAIClient(LLMClient):
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        try:
            from openai import AsyncOpenAI
        except ImportError as e:
            raise RuntimeError(
                "openai package not installed. Install with: pip install openai"
            ) from e
        if not os.environ.get("XAI_API_KEY"):
            raise RuntimeError("XAI_API_KEY not set.")
        self._client = AsyncOpenAI(
            api_key=os.environ["XAI_API_KEY"],
            base_url="https://api.x.ai/v1",
        )

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
        oai_tools = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.input_schema,
                },
            }
            for t in (tools or [])
        ] or None
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
                    args = json.loads(tc.function.arguments or "{}")
                    raw = tool.handler(args)
                    if inspect.isawaitable(raw):
                        raw = await raw
                    result = str(raw)
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
        return "Tool loop exceeded max_turns without final response."
