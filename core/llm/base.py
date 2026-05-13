# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""LLMClient ABC and shared dataclasses."""
from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Union


ToolHandler = Callable[[dict[str, Any]], Union[Any, Awaitable[Any]]]


def parse_tool_args(raw: Any, tool_name: str) -> dict[str, Any] | str:
    """Normalize tool-call arguments from any provider into a dict.

    Accepts:
      - JSON string (OpenAI / xAI shape)
      - dict or dict-like object (Gemini / Ollama shape — and Ollama
        sometimes hands back a JSON string instead, so both must work)
      - None (no arguments supplied)

    Returns the parsed dict on success. On JSONDecodeError or any
    coercion failure, returns an error string the tool loop can hand back
    to the model as the tool result — letting the model retry instead of
    crashing the agent.
    """
    if raw is None:
        return {}
    if isinstance(raw, str):
        try:
            return json.loads(raw or "{}")
        except json.JSONDecodeError as e:
            return f"error: malformed JSON arguments for tool {tool_name!r}: {e}"
    try:
        return dict(raw)
    except (TypeError, ValueError) as e:
        return f"error: cannot coerce arguments for tool {tool_name!r} to dict: {e}"


@dataclass
class Tool:
    """A tool callable across providers.

    `input_schema` is a JSON Schema object describing the input args.
    `handler` is invoked with the parsed input dict; may be sync or async.
    """

    name: str
    description: str
    input_schema: dict[str, Any]
    handler: ToolHandler


@dataclass
class LLMConfig:
    provider: str
    model: str
    auth_mode: str = "subscription"
    temperature: float = 0.3
    max_tokens: int = 4096
    system_prompt: str | None = None
    mcp_servers: dict[str, Any] = field(default_factory=dict)
    allowed_tools: list[str] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)


class LLMClient(ABC):
    """Provider-agnostic single-turn completion with optional tool use.

    The contract: take a system prompt + user message + optional tools,
    run the agent loop (tool calls auto-executed) until the model stops,
    return the final assistant text as a string.
    """

    def __init__(self, config: LLMConfig):
        self.config = config

    @abstractmethod
    async def complete(
        self,
        system_prompt: str,
        user_message: str,
        tools: list[Tool] | None = None,
    ) -> str:
        ...
