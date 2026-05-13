# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tests for core.config.load_config.

load_config reads `config.yaml` next to an agent file and merges sensible
defaults. These tests pin the default merging behavior so contributors
adding new providers don't accidentally break it.
"""
from __future__ import annotations

import pytest

from core.config import load_config


def _write_agent(tmp_path, yaml_body: str | None):
    """Create a fake agent dir with an agent.py + optional config.yaml.
    Returns the agent.py path to feed load_config."""
    agent_py = tmp_path / "agent.py"
    agent_py.write_text("# fake")
    if yaml_body is not None:
        (tmp_path / "config.yaml").write_text(yaml_body)
    return agent_py


def test_loads_explicit_fields(tmp_path):
    agent = _write_agent(
        tmp_path,
        """\
provider: openai
model: gpt-4o-mini
temperature: 0.7
max_tokens: 2048
""",
    )
    cfg = load_config(agent)
    assert cfg.provider == "openai"
    assert cfg.model == "gpt-4o-mini"
    assert cfg.temperature == 0.7
    assert cfg.max_tokens == 2048


def test_defaults_provider_to_claude_when_missing(tmp_path):
    agent = _write_agent(tmp_path, "temperature: 0.5\n")
    cfg = load_config(agent)
    assert cfg.provider == "claude"


def test_auth_mode_subscription_for_claude(tmp_path):
    agent = _write_agent(tmp_path, "provider: claude\n")
    cfg = load_config(agent)
    assert cfg.auth_mode == "subscription"


def test_auth_mode_api_key_for_non_claude(tmp_path):
    agent = _write_agent(tmp_path, "provider: openai\n")
    cfg = load_config(agent)
    assert cfg.auth_mode == "api_key"


def test_explicit_auth_mode_overrides_default(tmp_path):
    agent = _write_agent(tmp_path, "provider: openai\nauth_mode: subscription\n")
    cfg = load_config(agent)
    assert cfg.auth_mode == "subscription"


def test_default_model_falls_back_per_provider(tmp_path, monkeypatch):
    # Strip env-var overrides so we hit the hardcoded fallback table.
    for var in ("CLAUDE_MODEL", "OPENAI_MODEL", "GEMINI_MODEL", "XAI_MODEL"):
        monkeypatch.delenv(var, raising=False)
    agent = _write_agent(tmp_path, "provider: openai\n")
    cfg = load_config(agent)
    assert cfg.model == "gpt-4o"


def test_env_var_overrides_fallback_model(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o-2024-08-06")
    agent = _write_agent(tmp_path, "provider: openai\n")
    cfg = load_config(agent)
    assert cfg.model == "gpt-4o-2024-08-06"


def test_missing_config_yaml_raises(tmp_path):
    agent = _write_agent(tmp_path, None)
    with pytest.raises(FileNotFoundError):
        load_config(agent)


def test_empty_config_yaml_uses_all_defaults(tmp_path, monkeypatch):
    monkeypatch.delenv("CLAUDE_MODEL", raising=False)
    agent = _write_agent(tmp_path, "")
    cfg = load_config(agent)
    assert cfg.provider == "claude"
    assert cfg.model == "claude-sonnet-4-6"
    assert cfg.temperature == 0.3
    assert cfg.max_tokens == 4096
    assert cfg.mcp_servers == {}
    assert cfg.allowed_tools == []
    assert cfg.extra == {}


def test_passes_through_mcp_and_allowed_tools(tmp_path):
    agent = _write_agent(
        tmp_path,
        """\
provider: claude
allowed_tools:
  - WebSearch
  - Bash
mcp_servers:
  filesystem:
    command: npx
extra:
  max_turns: 8
""",
    )
    cfg = load_config(agent)
    assert cfg.allowed_tools == ["WebSearch", "Bash"]
    assert cfg.mcp_servers == {"filesystem": {"command": "npx"}}
    assert cfg.extra == {"max_turns": 8}
