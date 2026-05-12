# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Codex CLI adapter — experimental, NOT verified in v1.

Intent: invoke OpenAI's `codex` CLI binary the way our Claude adapter goes
through `claude-agent-sdk`. Codex CLI uses ChatGPT Plus / Pro subscription
auth (not the API console balance), so this would give users a fully
subscription-based path for OpenAI models — mirroring what we do with
Claude Max.

Status: stub. The maintainer doesn't currently have Codex CLI access to
verify behavior end-to-end. The CLI's non-interactive flags and JSON
output format are also still in flux at time of writing. Shipping
unverified code would violate the repo's "hand-built, tested" promise.

How to contribute the implementation:
    1. Install Codex CLI via OpenAI's official instructions
       (https://github.com/openai/codex) and log in to ChatGPT Plus/Pro.
    2. Read `codex --help` for the non-interactive invocation flags and
       the structured output format.
    3. Replace the bodies of `__init__` and `complete` below to spawn
       the CLI as a subprocess and parse its stdout.
    4. Update the row in `core/llm/factory.py`'s help text, the
       provider matrix in `README.md`, and the table in `AGENTS.md`
       from "stub" → "community-supported" or "verified".
"""
from __future__ import annotations

import shutil

from .base import LLMClient, LLMConfig, Tool


class CodexClient(LLMClient):
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        codex_present = shutil.which("codex") is not None
        hint = (
            "Codex CLI is installed at `codex` — the adapter itself is\n"
            "the missing piece. See the docstring of core/llm/codex.py\n"
            "and CONTRIBUTING.md for what needs implementing."
            if codex_present
            else "Codex CLI is not installed. Install via OpenAI's official\n"
                 "instructions: https://github.com/openai/codex"
        )
        raise NotImplementedError(
            "Codex CLI adapter is a stub in v1.\n\n"
            f"{hint}\n\n"
            "  - Verified providers: claude (default)\n"
            "  - Working providers:  openai, gemini, xai, ollama\n"
            "  - Stub:               codex (this provider)\n"
        )

    async def complete(
        self,
        system_prompt: str,
        user_message: str,
        tools: list[Tool] | None = None,
    ) -> str:
        raise NotImplementedError("Codex CLI adapter not implemented in v1.")
