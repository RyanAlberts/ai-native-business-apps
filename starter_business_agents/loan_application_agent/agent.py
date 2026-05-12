# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Loan & Funding Application Agent — match programs, prep package."""
from __future__ import annotations

import asyncio

from core import get_llm, load_config

from .prompts import SYSTEM_PROMPT
from .tools import all_tools


async def run(founder_description: str) -> str:
    """Match a founder to small-business funding programs and prep package.

    Args:
        founder_description: Free-text covering the business, stage,
            current revenue, funding amount needed, what it's for,
            founder credit / collateral situation, location.

    Returns:
        Markdown with sections per `prompts.SYSTEM_PROMPT`.
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
        "Two-year-old LLC bakery in Boise, Idaho. ~$280k revenue last year, "
        "trending +30% YoY. Need ~$120k to buy a second oven, expand the "
        "kitchen, and add one delivery van. Founder has 720 credit, owns "
        "home (~$120k equity), no other business debt."
    )
    desc = " ".join(sys.argv[1:]) or default
    print(asyncio.run(run(desc)))
