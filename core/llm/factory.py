# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Factory: build the right LLMClient for a config."""
from __future__ import annotations

from .base import LLMClient, LLMConfig


def get_llm(config: LLMConfig) -> LLMClient:
    provider = config.provider.lower()
    if provider == "claude":
        from .claude import ClaudeClient
        return ClaudeClient(config)
    if provider == "openai":
        from .openai import OpenAIClient
        return OpenAIClient(config)
    if provider == "gemini":
        from .gemini import GeminiClient
        return GeminiClient(config)
    if provider == "xai":
        from .xai import XAIClient
        return XAIClient(config)
    if provider == "ollama":
        from .ollama import OllamaClient
        return OllamaClient(config)
    if provider == "codex":
        from .codex import CodexClient
        return CodexClient(config)
    raise ValueError(
        f"Unknown provider: {config.provider!r}. "
        f"Expected one of: claude, openai, gemini, xai, ollama, codex."
    )
