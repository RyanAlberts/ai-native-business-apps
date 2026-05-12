# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Business Idea Validator — example template agent.

A self-contained single-agent template. Copy this folder to
`starter_business_agents/NN_<your_agent>/`, then customize:

  1. Edit `prompts.py` — change the system prompt to your role.
  2. Edit `tools.py`   — add any custom @tool functions you need.
  3. Edit `config.yaml`— pick provider (claude/openai/gemini/...) and model.
  4. Update this docstring and `README.md` to describe what your agent does.
"""
from __future__ import annotations

import asyncio

from core import get_llm, load_config

from .prompts import SYSTEM_PROMPT
from .tools import all_tools


async def run(idea: str) -> str:
    """Validate a startup business idea. Returns a markdown analysis."""
    config = load_config(__file__)
    llm = get_llm(config)
    return await llm.complete(
        system_prompt=SYSTEM_PROMPT,
        user_message=f"Validate this business idea:\n\n{idea}",
        tools=all_tools(),
    )


if __name__ == "__main__":
    import sys
    idea = " ".join(sys.argv[1:]) or "An AI-powered shopping list app for busy parents."
    print(asyncio.run(run(idea)))
