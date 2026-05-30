# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""83(b) Election Agent — prepare and time the IRS §83(b) election for restricted stock.

Why this exists: founders who receive restricted stock subject to vesting have
30 calendar days from the grant/transfer date to file an §83(b) election. Miss
the window and you owe ordinary income tax on every vesting tranche for the
next 4 years on the spread between FMV and the price paid — frequently a
five- to six-figure mistake.

Stripe Atlas auto-files this for founders who incorporated through them.
Everyone else routinely misses it. This agent gives any founder — regardless
of where they formed — a ready-to-mail 83(b) election letter, a postmark
deadline, the right IRS service center address, and a calendar reminder file.

LegalZoom-equivalent service: none (they don't sell §83(b)). Stripe Atlas
charges nothing for it but only as a bundle with their $500 formation product.
This agent is free + open source.

NOT legal or tax advice. The output is a starting draft a CPA or attorney
should review before signing and mailing.
"""
from __future__ import annotations

import asyncio

from core import build_user_message, get_llm, load_config

from .prompts import SYSTEM_PROMPT
from .tools import all_tools


async def run(founder_input) -> str:
    """Prepare a §83(b) election letter, deadline check, and mailing kit.

    `founder_input` should describe the founder, the company, the shares
    received, the date of grant, the FMV, the price paid, and the vesting /
    repurchase restrictions. It accepts free text or a shared ``Company``
    profile (dict / ``company.json`` path / raw JSON also work) — known facts
    are threaded in. The agent asks clarifying questions in its output if
    anything is missing rather than fabricating values.
    """
    config = load_config(__file__)
    llm = get_llm(config)
    return await llm.complete(
        system_prompt=SYSTEM_PROMPT,
        user_message=build_user_message(
            founder_input,
            template="Prepare an 83(b) election for this situation:\n\n{input}",
        ),
        tools=all_tools(),
    )


if __name__ == "__main__":
    import sys
    example = (
        "Solo founder Jane Doe, SSN 123-45-6789, residing at 123 Main St, "
        "Austin TX 78701. Granted 8,000,000 shares of common stock of "
        "Acme Books Inc. (Delaware C-Corp, EIN 88-1234567) on 2026-05-01 at "
        "$0.0001/share par value. FMV at grant: $0.0001/share. Vesting: "
        "4-year monthly with 1-year cliff, company repurchase right on unvested."
    )
    prompt = " ".join(sys.argv[1:]) or example
    print(asyncio.run(run(prompt)))
