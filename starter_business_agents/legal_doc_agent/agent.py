# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Legal Document Generator — draft operating agreements, NDAs, IP assignments, ToS, etc."""
from __future__ import annotations

import asyncio

from core import build_user_message, get_llm, load_config

from .prompts import SYSTEM_PROMPT
from .tools import all_tools


async def run(request) -> str:
    """Draft a legal document for review by counsel.

    Args:
        request: Free-text request including document type, business context,
            parties, and any special terms. E.g. "Single-member LLC Operating
            Agreement for a Delaware-formed SaaS consultancy operating in CA."
            A shared ``Company`` profile (or dict / ``company.json`` path /
            raw JSON) is also accepted — its facts are threaded in, though you
            still need to say which document you want in the company notes.

    Returns:
        Markdown including the draft document + key-clause explanations.
    """
    config = load_config(__file__)
    llm = get_llm(config)
    return await llm.complete(
        system_prompt=SYSTEM_PROMPT,
        user_message=build_user_message(request),
        tools=all_tools(),
    )


if __name__ == "__main__":
    import sys
    default = (
        "Draft a Mutual NDA for a software founder negotiating with a "
        "potential enterprise customer. Parties: Founder LLC (Delaware) "
        "and AcmeCorp Inc. Term: 2 years from disclosure. Governing law: "
        "Delaware. No specific industry triggers."
    )
    desc = " ".join(sys.argv[1:]) or default
    print(asyncio.run(run(desc)))
