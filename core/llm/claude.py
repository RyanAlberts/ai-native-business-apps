# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Claude adapter — uses claude-agent-sdk.

Default: subscription auth via the `claude` CLI. Three legitimate auth modes:

  1. **Plain subscription** — user has run `claude login` once; no
     `ANTHROPIC_API_KEY` in their shell. The SDK spawns the `claude`
     binary which uses the stored Max/Pro credentials. ZERO cost.

  2. **Inside Claude Code app / Cursor with Claude integration** — the
     host IDE injects an OAuth-refreshed `ANTHROPIC_API_KEY` that's tied
     to the user's subscription, not a paid API account. We detect this
     via env markers (`CLAUDECODE`, `CLAUDE_CODE_ENTRYPOINT`, etc.) and
     let it pass through — the user is already paying via subscription.

  3. **Paid API key (explicit opt-in)** — user set
     `ANTHROPIC_API_KEY` themselves AND `ALLOW_API_KEY=1`. Billed
     against Anthropic console balance.

The guard exists to prevent case (3) happening accidentally because the
user pasted an API key into their shell rc file and forgot.
"""
from __future__ import annotations

import inspect
import os

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    create_sdk_mcp_server,
    query,
    tool as sdk_tool,
)

from .base import LLMClient, LLMConfig, Tool


# Env markers set by IDEs that inject an OAuth-refreshed subscription token
# rather than a paid API key. If any of these is set, we treat the
# ANTHROPIC_API_KEY as subscription-billed.
_OAUTH_IDE_MARKERS = (
    "CLAUDECODE",                              # Claude Code app sets =1
    "CLAUDE_CODE_ENTRYPOINT",                  # Claude Code's entrypoint marker
    "CLAUDE_CODE_SDK_HAS_OAUTH_REFRESH",       # Explicit OAuth signal
    "CURSOR_CLAUDE_OAUTH",                     # Reserved for future Cursor integration
)


class ClaudeClient(LLMClient):
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self._enforce_subscription_guard()

    def _enforce_subscription_guard(self) -> None:
        api_key_set = bool(os.environ.get("ANTHROPIC_API_KEY"))
        if not api_key_set or self.config.auth_mode != "subscription":
            return
        # API key IS set in subscription mode. Three exits:
        if os.environ.get("ALLOW_API_KEY") == "1":
            return  # explicit user override
        if any(os.environ.get(m) for m in _OAUTH_IDE_MARKERS):
            return  # running inside an IDE that auths via OAuth-refreshed token
        raise RuntimeError(
            "ANTHROPIC_API_KEY is set but config.yaml requests subscription auth.\n"
            "  - If you're inside Claude Code / Cursor: this normally passes\n"
            "    through automatically; check that CLAUDECODE or\n"
            "    CLAUDE_CODE_ENTRYPOINT is set in your env.\n"
            "  - To use plain subscription (free, via Claude Max): unset\n"
            "    ANTHROPIC_API_KEY.\n"
            "  - To use a paid API key (you'll be billed): set\n"
            "    ALLOW_API_KEY=1 in your env."
        )

    async def complete(
        self,
        system_prompt: str,
        user_message: str,
        tools: list[Tool] | None = None,
    ) -> str:
        mcp_servers, allowed = self._build_tools(tools)
        options = ClaudeAgentOptions(
            model=self.config.model,
            system_prompt=system_prompt,
            mcp_servers=mcp_servers,
            allowed_tools=allowed,
            permission_mode=self._permission_mode(),
            max_turns=self.config.extra.get("max_turns", 25),
            # Isolate from host environment: don't auto-load the user's
            # global / project / local Claude settings (skills, plugins,
            # hooks). Each agent is a clean session — reproducible whether
            # the user is in Claude Code, Cursor, or a plain terminal.
            setting_sources=[],
        )

        last_text = ""
        async for msg in query(prompt=user_message, options=options):
            if isinstance(msg, ResultMessage):
                if getattr(msg, "result", None):
                    last_text = msg.result
            elif isinstance(msg, AssistantMessage):
                for block in getattr(msg, "content", []) or []:
                    if isinstance(block, TextBlock):
                        last_text = block.text
        return last_text

    def _permission_mode(self) -> str:
        """Resolve the SDK permission mode, safely for root environments.

        Default is ``bypassPermissions`` — right for an unattended agent on a
        normal user account. But the underlying ``claude`` CLI refuses
        ``--dangerously-skip-permissions`` under root/sudo and exits 1, so a
        plain ``bypassPermissions`` default would make every agent fail in
        root containers / CI out of the box.

        Resolution order:
          1. An explicit ``extra.permission_mode`` in config.yaml always wins.
          2. Else the ``KEEL_PERMISSION_MODE`` env var, if set — lets you
             override every agent at once without editing each config.yaml.
          3. Otherwise default to ``bypassPermissions``, but transparently
             downgrade to ``default`` when running as root so the agent still
             runs instead of crashing.
        """
        explicit = self.config.extra.get("permission_mode") or os.environ.get(
            "KEEL_PERMISSION_MODE"
        )
        if explicit:
            return explicit
        is_root = hasattr(os, "geteuid") and os.geteuid() == 0
        return "default" if is_root else "bypassPermissions"

    def _build_tools(
        self, tools: list[Tool] | None
    ) -> tuple[dict, list[str]]:
        mcp_servers: dict = dict(self.config.mcp_servers or {})
        allowed: list[str] = list(self.config.allowed_tools or [])
        if not tools:
            return mcp_servers, allowed

        sdk_tools = [_wrap(t) for t in tools]
        server_name = "local"
        mcp_servers[server_name] = create_sdk_mcp_server(
            name=server_name, version="1.0.0", tools=sdk_tools
        )
        allowed.extend(f"mcp__{server_name}__{t.name}" for t in tools)
        return mcp_servers, allowed


def _wrap(t: Tool):
    """Wrap a provider-agnostic Tool as a claude-agent-sdk SdkMcpTool."""
    name = t.name
    description = t.description
    schema = t.input_schema
    handler = t.handler

    async def _impl(args):
        result = handler(args)
        if inspect.isawaitable(result):
            result = await result
        if isinstance(result, dict) and "content" in result:
            return result
        return {"content": [{"type": "text", "text": str(result)}]}

    _impl.__name__ = name
    return sdk_tool(name, description, schema)(_impl)
