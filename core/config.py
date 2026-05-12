# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Load per-agent config.yaml and merge env-var overrides."""
from __future__ import annotations

import os
from pathlib import Path

import yaml

from .llm import LLMConfig


def load_config(agent_file: str | Path) -> LLMConfig:
    """Load `config.yaml` from the directory of the calling agent file.

    Usage:
        from core import load_config
        cfg = load_config(__file__)
    """
    agent_dir = Path(agent_file).resolve().parent
    config_path = agent_dir / "config.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"config.yaml not found at {config_path}")
    raw = yaml.safe_load(config_path.read_text()) or {}

    provider = raw.get("provider", "claude")
    model = raw.get("model") or _default_model(provider)
    return LLMConfig(
        provider=provider,
        model=model,
        auth_mode=raw.get("auth_mode", "subscription" if provider == "claude" else "api_key"),
        temperature=float(raw.get("temperature", 0.3)),
        max_tokens=int(raw.get("max_tokens", 4096)),
        system_prompt=raw.get("system_prompt"),
        mcp_servers=raw.get("mcp_servers", {}),
        allowed_tools=raw.get("allowed_tools", []),
        extra=raw.get("extra", {}),
    )


_DEFAULTS = {
    "claude": "CLAUDE_MODEL",
    "openai": "OPENAI_MODEL",
    "gemini": "GEMINI_MODEL",
    "xai": "XAI_MODEL",
    "ollama": "OLLAMA_MODEL",
    "codex": "CODEX_MODEL",
}

_FALLBACK = {
    "claude": "claude-sonnet-4-6",
    "openai": "gpt-4o",
    "gemini": "gemini-2.0-flash",
    "xai": "grok-2-latest",
    "ollama": "llama3.2",
    "codex": "gpt-4o",
}


def _default_model(provider: str) -> str:
    env_var = _DEFAULTS.get(provider)
    if env_var and os.environ.get(env_var):
        return os.environ[env_var]
    return _FALLBACK.get(provider, "claude-sonnet-4-6")
