# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Bank & Insurance Setup Agent — recommend account + policies + 30-day plan."""
from __future__ import annotations

import asyncio

from core import get_llm, load_config

from .prompts import SYSTEM_PROMPT
from .tools import all_tools


async def run(founder_description: str) -> str:
    """Recommend a business bank + insurance policies for a small business.

    Args:
        founder_description: Free-text covering business type, state,
            revenue stage, employee count, products/services, risk profile.

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
        "Two-person LLC, software consulting for healthcare clinics. "
        "Operating from California, formed in Delaware. ~$200k revenue. "
        "Store customer-data summaries (no PHI). No physical office. "
        "Both cofounders are full-time on the business; no other employees."
    )
    desc = " ".join(sys.argv[1:]) or default
    print(asyncio.run(run(desc)))
