# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Worker Classification Agent — 1099 contractor vs W-2 employee.

Misclassification is one of the most common and expensive payroll
mistakes founders make: a finding can mean back payroll taxes, penalties,
and multi-year retroactive assessments. The trap everyone falls into:
treating a full-time role as 1099 to dodge payroll. The "Independent
Contractor Agreement" the founder hands the worker does NOT settle the
issue — courts and agencies look at the actual relationship.

This agent applies the IRS three-category common-law test + the DOL
six-factor economic-reality test (2024 Final Rule — note the DOL is not
currently enforcing it; see FAB 2025-1), then layers on state-specific
rules (California AB5 / Massachusetts / New Jersey ABC tests force W-2 if
any of A, B, or C fails, regardless of federal-test outcome).

NOT legal advice. Always validate with an employment attorney or PEO/HRIS
provider before issuing the contract or paying the worker.
"""
from __future__ import annotations

import asyncio

from core import build_user_message, get_llm, load_config

from .prompts import SYSTEM_PROMPT
from .tools import all_tools


async def run(founder_input) -> str:
    """Classify a role as 1099 or W-2 with structured analysis + risk score.

    Accepts free text or a shared ``Company`` profile (dict / ``company.json``
    path / raw JSON also work); known facts are threaded in automatically.
    """
    config = load_config(__file__)
    llm = get_llm(config)
    return await llm.complete(
        system_prompt=SYSTEM_PROMPT,
        user_message=build_user_message(
            founder_input, template="Classify this role:\n\n{input}"
        ),
        tools=all_tools(),
    )


if __name__ == "__main__":
    import sys
    example = (
        "I'm a 5-person software startup in San Francisco, CA. I want to "
        "hire a 'contractor' to be our lead engineer — full-time hours "
        "(40/wk), Monday-Friday 9-5, working from our office on a laptop "
        "we'd provide. We'd pay $150/hr, no benefits. We want to call "
        "them a 1099 to avoid payroll burden. Is this okay?"
    )
    prompt = " ".join(sys.argv[1:]) or example
    print(asyncio.run(run(prompt)))
