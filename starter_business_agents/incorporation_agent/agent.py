# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Incorporation Agent — recommend entity type, state, and filing plan."""
from __future__ import annotations

import asyncio

from core import build_user_message, get_llm, load_config

from .prompts import SYSTEM_PROMPT
from .tools import all_tools


async def run(founder_description) -> str:
    """Generate an incorporation plan from a founder description.

    Args:
        founder_description: a free-text description, or a shared ``Company``
            profile (also accepts a dict, a ``company.json`` path, or raw
            JSON). When a profile is given, its facts are threaded in so the
            agent doesn't re-ask for them.

    Returns:
        Markdown with sections defined in `prompts.SYSTEM_PROMPT`.
    """
    config = load_config(__file__)
    llm = get_llm(config)
    return await llm.complete(
        system_prompt=SYSTEM_PROMPT,
        user_message=build_user_message(founder_description),
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
