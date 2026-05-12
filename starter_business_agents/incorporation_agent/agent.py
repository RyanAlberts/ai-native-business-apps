# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Incorporation Agent — recommend entity type, state, and filing plan."""
from __future__ import annotations

import asyncio

from core import get_llm, load_config

from .prompts import SYSTEM_PROMPT
from .tools import all_tools


async def run(founder_description: str) -> str:
    """Generate an incorporation plan from a free-text founder description.

    Args:
        founder_description: Free-text covering business name & idea, founder
            home state, # cofounders, revenue/funding plans, employees (or not),
            and any liability concerns.

    Returns:
        Markdown with sections defined in `prompts.SYSTEM_PROMPT`.
    """
    config = load_config(__file__)
    llm = get_llm(config)
    return await llm.complete(
        system_prompt=SYSTEM_PROMPT,
        user_message=founder_description,
        tools=all_tools(),
    )


if __name__ == "__main__":
    import sys
    default = (
        "Two-cofounder SaaS for accounting firms. We're based in Texas. "
        "We plan to raise a seed round in 9 months, hire 2 engineers within "
        "a year, and start charging customers in Q4."
    )
    desc = " ".join(sys.argv[1:]) or default
    print(asyncio.run(run(desc)))
