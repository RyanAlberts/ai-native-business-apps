# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tests for the Claude adapter's permission-mode resolution.

Regression coverage for the root/sudo bug: the SDK's default
``bypassPermissions`` makes the underlying CLI pass
``--dangerously-skip-permissions``, which it refuses under root and exits 1.
The adapter must downgrade to ``default`` as root while still honoring an
explicit config override.

These tests construct the client with auth_mode other than "subscription" so
the subscription guard is a no-op and no real CLI/network is touched —
``_permission_mode`` is pure logic.
"""
from __future__ import annotations

import os

from core import LLMConfig
from core.llm.claude import ClaudeClient


def _client(**extra):
    return ClaudeClient(
        LLMConfig(provider="claude", model="m", auth_mode="api", extra=extra)
    )


def test_explicit_override_always_wins(monkeypatch):
    monkeypatch.setattr(os, "geteuid", lambda: 0, raising=False)
    assert _client(permission_mode="acceptEdits")._permission_mode() == "acceptEdits"
    monkeypatch.setattr(os, "geteuid", lambda: 1000, raising=False)
    assert _client(permission_mode="plan")._permission_mode() == "plan"


def test_default_downgrades_to_default_as_root(monkeypatch):
    monkeypatch.setattr(os, "geteuid", lambda: 0, raising=False)
    assert _client()._permission_mode() == "default"


def test_default_bypasses_for_normal_user(monkeypatch):
    monkeypatch.delenv("KEEL_PERMISSION_MODE", raising=False)
    monkeypatch.setattr(os, "geteuid", lambda: 1000, raising=False)
    assert _client()._permission_mode() == "bypassPermissions"


def test_env_var_overrides_default_but_not_config(monkeypatch):
    monkeypatch.setenv("KEEL_PERMISSION_MODE", "plan")
    # env var beats the bypass/root default
    assert _client()._permission_mode() == "plan"
    # explicit config still wins over the env var
    assert _client(permission_mode="acceptEdits")._permission_mode() == "acceptEdits"
