# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Ollama adapter — local Llama/Qwen/Mistral via Ollama daemon (default localhost:11434)."""
from __future__ import annotations

import inspect

from .base import LLMClient, LLMConfig, Tool, parse_tool_args


class OllamaClient(LLMClient):
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        try:
            from ollama import AsyncClient
        except ImportError as e:
            raise RuntimeError(
                "ollama package not installed. Install with: pip install ollama"
            ) from e
        host = config.extra.get("host", "http://localhost:11434")
        self._client = AsyncClient(host=host)

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
        ollama_tools = [
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
            resp = await self._client.chat(
                model=self.config.model,
                messages=messages,
                tools=ollama_tools,
                options={
                    "temperature": self.config.temperature,
                    "num_predict": self.config.max_tokens,
                },
            )
            msg = resp.get("message") if isinstance(resp, dict) else resp.message
            calls = (msg.get("tool_calls") if isinstance(msg, dict) else msg.tool_calls) or []
            if not calls:
                return (msg.get("content") if isinstance(msg, dict) else msg.content) or ""
            messages.append(dict(msg) if not isinstance(msg, dict) else msg)
            for tc in calls:
                fn = tc.get("function") if isinstance(tc, dict) else tc.function
                fname = fn.get("name") if isinstance(fn, dict) else fn.name
                fargs = fn.get("arguments") if isinstance(fn, dict) else fn.arguments
                tool = tool_map.get(fname)
                if not tool:
                    result = f"unknown tool: {fname}"
                else:
                    args = parse_tool_args(fargs, fname)
                    if isinstance(args, str):
                        result = args
                    else:
                        raw = tool.handler(args)
                        if inspect.isawaitable(raw):
                            raw = await raw
                        result = str(raw)
                messages.append({"role": "tool", "content": result, "tool_name": fname})
        return "Tool loop exceeded max_turns without final response."
