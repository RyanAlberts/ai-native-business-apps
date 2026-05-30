# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Business License + DBA Agent.

Identifies EVERY license, permit, and DBA registration the founder needs
at the federal / state / county / city level for their specific
situation — across an industry, a city, and a state. Uses two
deterministic tools (DBA filing jurisdiction by state; general state
license requirement) plus WebSearch for the long-tail city/county
specifics.

LegalZoom and PEOs do not handle city/county-level licenses; "business
license services" charge $99-$300 per location. This agent: $0.

NOT legal advice. Licensing requirements change. Always verify on the
issuing agency's current site before paying.
"""
from __future__ import annotations

import asyncio

from core import build_user_message, get_llm, load_config

from .prompts import SYSTEM_PROMPT
from .tools import all_tools


async def run(founder_input) -> str:
    """Produce a city/county/state/federal license + permit + DBA checklist.

    Accepts free text or a shared ``Company`` profile (dict / ``company.json``
    path / raw JSON also work); known facts are threaded in automatically.
    """
    config = load_config(__file__)
    llm = get_llm(config)
    return await llm.complete(
        system_prompt=SYSTEM_PROMPT,
        user_message=build_user_message(
            founder_input,
            template="What licenses and permits do I need?\n\n{input}",
        ),
        tools=all_tools(),
    )


if __name__ == "__main__":
    import sys
    example = (
        "I'm forming an LLC in California to operate a small specialty coffee "
        "shop. Principal location: 1234 Mission St, San Francisco, CA 94110 "
        "(San Francisco County). We'll have an on-premise kitchen serving "
        "pastries baked on-site, indoor + sidewalk seating, beer/wine "
        "license planned for evenings. Two employees year 1. The LLC will "
        "be 'Mission Coffee LLC' but we'll operate as 'The Daily Grind'. "
        "What licenses and permits do I need, in what order, and what will "
        "it cost?"
    )
    prompt = " ".join(sys.argv[1:]) or example
    print(asyncio.run(run(prompt)))
