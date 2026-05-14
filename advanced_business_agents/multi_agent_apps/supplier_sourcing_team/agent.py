# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Supplier Sourcing Team — sequential 4-stage pipeline.

Stage 1: Sourcing (long list, category map, geography strategy)
Stage 2: Vetting (criteria, qualifying questions, red flags)
Stage 3: RFP draft (ready-to-send Request for Proposal)
Stage 4: Comparison (matrix template, scoring rubric, negotiation playbook)
"""
from __future__ import annotations

import asyncio

from core import HarnessResult, SequentialHarness, Stage, get_llm, load_config

from .prompts import (
    COMPARISON_PROMPT,
    RFP_PROMPT,
    SOURCING_PROMPT,
    VETTING_PROMPT,
)
from .tools import all_tools


def _stages() -> list[Stage]:
    tools = all_tools()
    return [
        Stage(name="Sourcing", system_prompt=SOURCING_PROMPT, tools=tools),
        Stage(
            name="Vetting",
            system_prompt=VETTING_PROMPT,
            input_template="Sourcing brief:\n\n{input}",
        ),
        Stage(
            name="RFP Draft",
            system_prompt=RFP_PROMPT,
            input_template="Sourcing + vetting:\n\n{input}",
        ),
        Stage(
            name="Comparison Matrix",
            system_prompt=COMPARISON_PROMPT,
            input_template="Preceding stages:\n\n{input}",
        ),
    ]


async def run(sourcing_need: str, on_stage_complete=None) -> HarnessResult:
    """Run the 4-stage supplier sourcing pipeline.

    Args:
        sourcing_need: Free-text describing what's being sourced — category,
            volume, budget, timeline, quality bar, geography preferences.
        on_stage_complete: Optional `(stage_name, output)` callback.

    Returns:
        HarnessResult — `final` is the comparison matrix; `stages` has all 4.
    """
    config = load_config(__file__)
    llm = get_llm(config)
    harness = SequentialHarness(llm=llm, stages=_stages())
    return await harness.run(sourcing_need, on_stage_complete=on_stage_complete)


if __name__ == "__main__":
    import sys
    default = (
        "Need to source contract-manufactured silicone kitchenware for a "
        "DTC ecommerce brand. Volume: initial 5,000 units across 3 SKUs, "
        "projected 50,000 units year 1. Budget: $4/unit landed. Quality: "
        "FDA food-safe certified. Timeline: first samples in 6 weeks, "
        "production order in 10 weeks. Open to US, Mexico, or Asia."
    )
    desc = " ".join(sys.argv[1:]) or default

    def progress(name: str, output: str) -> None:
        # flush=True so partial progress is visible if the run is killed.
        print(f"\n{'='*70}\n  Stage complete: {name}\n{'='*70}", flush=True)
        print(output[:400] + ("..." if len(output) > 400 else ""), flush=True)

    result = asyncio.run(run(desc, on_stage_complete=progress))
    print(f"\n{'='*70}\n  COMPARISON MATRIX\n{'='*70}")
    print(result.final)
