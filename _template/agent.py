# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Business Idea Validator — the canonical Claude Agent SDK pattern.

This file is the reference example for how every agent in this repo is built.
The shape never changes; only the prompts, tools, and config differ.

────────────────────────────────────────────────────────────────────────────
The Agent SDK pattern in 4 lines
────────────────────────────────────────────────────────────────────────────

    config = load_config(__file__)                # reads config.yaml
    llm    = get_llm(config)                      # ClaudeClient by default
    result = await llm.complete(                  # one SDK round-trip
        system_prompt=SYSTEM_PROMPT,
        user_message=user_input,
        tools=all_tools(),                        # list[core.Tool]
    )

`get_llm()` returns a `ClaudeClient` whose `complete()` method internally
constructs `ClaudeAgentOptions(model=..., system_prompt=..., mcp_servers=...,
allowed_tools=..., setting_sources=[], permission_mode="bypassPermissions")`
and iterates `claude_agent_sdk.query(prompt=..., options=options)` until the
final `ResultMessage` arrives. We never touch the SDK directly — the
abstraction in `core/llm/claude.py` is the single place that knows about
`claude-agent-sdk`.

────────────────────────────────────────────────────────────────────────────
Why this matters (the value of the SDK)
────────────────────────────────────────────────────────────────────────────

1. **Max 20x billing (post-June 15, 2026).** SDK calls draw on a separate
   $200/mo credit, leaving your interactive Claude Code / chat limits free.

2. **MCP tool routing.** Every `core.Tool` in `tools.py::all_tools()` gets
   wrapped into a `create_sdk_mcp_server` server and exposed to the model
   via `mcp__local__<tool_name>`. The SDK loops tool calls automatically.

3. **Session isolation.** `setting_sources=[]` means the agent ignores the
   host's user/project/local Claude settings — no plugin / hook leakage
   even when running inside Claude Code or Cursor.

────────────────────────────────────────────────────────────────────────────
How to fork this template into your own agent
────────────────────────────────────────────────────────────────────────────

  1. Copy this folder to `starter_business_agents/<your_agent>/`.
  2. Edit `prompts.py::SYSTEM_PROMPT` — change the role + output format.
  3. Edit `tools.py::all_tools()` — return `core.Tool` instances.
  4. Edit `config.yaml` — provider, model, MCP servers, allowed_tools.
  5. Update `run()`'s signature + docstring below.
  6. Rewrite README.md / WALKTHROUGH.md / PARITY.md for your domain.

  Multi-stage pipelines (e.g. Research → Strategy → Roadmap)? Use
  `core.SequentialHarness` instead of a single `complete()` call. See
  `advanced_business_agents/multi_agent_apps/business_plan_implementation_manager/`
  for a working 4-stage example.
"""
from __future__ import annotations

import asyncio

from core import get_llm, load_config

from .prompts import SYSTEM_PROMPT
from .tools import all_tools


async def run(idea: str) -> str:
    """Validate a startup business idea via the Claude Agent SDK.

    Args:
        idea: One-paragraph description of the business idea.

    Returns:
        Markdown analysis with sections: Problem, Target customer, MVP scope,
        Top 3 risks, First experiment.
    """
    # 1. Load this agent's config.yaml (provider, model, tools, etc.)
    config = load_config(__file__)

    # 2. Build the right LLM client. Default is ClaudeClient, which wraps
    #    claude-agent-sdk. Swap provider in config.yaml to use openai /
    #    gemini / xai / ollama instead — the call below stays identical.
    llm = get_llm(config)

    # 3. One round-trip through the Agent SDK. Handles tool loop, MCP
    #    routing, and final-result extraction internally.
    return await llm.complete(
        system_prompt=SYSTEM_PROMPT,
        user_message=f"Validate this business idea:\n\n{idea}",
        tools=all_tools(),
    )


if __name__ == "__main__":
    import sys
    idea = " ".join(sys.argv[1:]) or "An AI-powered shopping list app for busy parents."
    print(asyncio.run(run(idea)))
