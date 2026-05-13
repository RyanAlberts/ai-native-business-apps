# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Worker Classification Agent — 1099 contractor vs W-2 employee.

40% of US small businesses get a misclassification finding in an IRS or
state DOL audit. Average penalty: $845, plus back payroll-tax assessments
on multi-year lookback windows. The mistake everyone makes: treating a
full-time role as 1099 to dodge payroll. The "Independent Contractor
Agreement" the founder hands the worker does NOT settle the issue —
courts and agencies look at the actual relationship.

This agent applies the IRS three-category common-law test + the DOL 2024
six-factor economic-reality test, then layers on state-specific rules
(California AB5 / Massachusetts / New Jersey ABC tests force W-2 if any
of A, B, or C fails, regardless of federal-test outcome).

NOT legal advice. Always validate with an employment attorney or PEO/HRIS
provider before issuing the contract or paying the worker.
"""
from __future__ import annotations

import asyncio

from core import get_llm, load_config

from .prompts import SYSTEM_PROMPT
from .tools import all_tools


async def run(founder_input: str) -> str:
    """Classify a role as 1099 or W-2 with structured analysis + risk score."""
    config = load_config(__file__)
    llm = get_llm(config)
    return await llm.complete(
        system_prompt=SYSTEM_PROMPT,
        user_message=f"Classify this role:\n\n{founder_input}",
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
