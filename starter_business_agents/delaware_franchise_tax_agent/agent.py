# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Delaware Franchise Tax Calculator agent.

Computes Delaware C-Corp franchise tax under BOTH methods (Authorized
Shares default vs Assumed Par Value Capital) and tells the founder which
to elect on their March 1 filing.

The default Authorized Shares method bills a typical early-stage startup
(10M authorized, 8M issued, par $0.0001, year-end assets ~$50K) **$85,000**.
The Assumed Par Value Capital method, on the same filing, bills the same
startup **$400**.

Founders panic-pay the wrong number constantly. Carta charges to fix it.
This agent does it free.

NOT legal or tax advice. The output assumes the founder's gross-assets
number is correct — that's the one input that depends on their books and
should be CPA-verified.
"""
from __future__ import annotations

import asyncio

from core import build_user_message, get_llm, load_config

from .prompts import SYSTEM_PROMPT
from .tools import all_tools


async def run(founder_input) -> str:
    """Compute DE franchise tax and explain the recommended method.

    Accepts free text or a shared ``Company`` profile (dict / ``company.json``
    path / raw JSON also work); known facts are threaded in automatically.
    """
    config = load_config(__file__)
    llm = get_llm(config)
    return await llm.complete(
        system_prompt=SYSTEM_PROMPT,
        user_message=build_user_message(
            founder_input,
            template="Help me with my Delaware franchise tax bill:\n\n{input}",
        ),
        tools=all_tools(),
    )


if __name__ == "__main__":
    import sys
    example = (
        "I just got a Delaware franchise tax bill for $85,165 and I'm "
        "freaking out. We're a 12-month-old C-Corp formed in Delaware. "
        "10,000,000 authorized shares, 8,000,000 issued, par value "
        "$0.0001. Total assets at year-end were about $50,000. Is the "
        "$85K bill real?"
    )
    prompt = " ".join(sys.argv[1:]) or example
    print(asyncio.run(run(prompt)))
