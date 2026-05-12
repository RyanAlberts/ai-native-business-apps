# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Compliance & Tax Setup Agent — nexus + filings + bookkeeping plan."""
from __future__ import annotations

import asyncio

from core import get_llm, load_config

from .prompts import SYSTEM_PROMPT
from .tools import all_tools


async def run(founder_description: str) -> str:
    """Generate a compliance and tax setup plan.

    Args:
        founder_description: Free-text covering entity type, formation
            state, states of operation, products/services, sales channels,
            employees, expected revenue.

    Returns:
        Markdown per `prompts.SYSTEM_PROMPT`.
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
        "Delaware LLC, operating from California. E-commerce skincare brand "
        "selling on Shopify (own site) + Amazon. Year 1 revenue ~$200k. "
        "Customers in all 50 states. No employees, just the solo founder. "
        "Inventory stored at California 3PL plus Amazon FBA warehouses."
    )
    desc = " ".join(sys.argv[1:]) or default
    print(asyncio.run(run(desc)))
