# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Trademark Search Team — multi-sub-agent showcase.

Fans out four research branches concurrently against the same proposed
mark + goods/services description, then synthesizes a likelihood-of-
confusion verdict + TEAS application pre-fill + USPTO fee estimate.

Branches (run in parallel):
    1. Federal TESS search          (WebSearch)
    2. State-level trademark search (WebSearch)
    3. Common-law conflict scan     (WebSearch)
    4. USPTO Nice class ID          (WebSearch)

Synthesizer (runs after all four return):
    - Reads all four branch outputs
    - Calls `uspto_fee_estimate` tool (deterministic)
    - Produces verdict (GO / CAUTION / NO-GO), conflicts table,
      class recommendation, fee estimate, TEAS application pre-fill,
      calendar deadlines, and next steps.

What this replaces:
    - LegalZoom federal search: $199
    - LegalZoom comprehensive (federal + state + common-law): $299
    - LegalZoom registration package: $899 + USPTO fees
    - Boutique trademark attorney pre-filing review: $500-$1,500

This agent: $0. The actual USPTO filing fee still goes to USPTO.

NOT legal advice. The output is a search + draft, not a filed
application. Trademark conflicts are fact-intensive and §2(d)
examination is subjective — a CAUTION or NO-GO verdict warrants
attorney review before filing.
"""
from __future__ import annotations

import asyncio

from core import (
    HarnessResult,
    ParallelHarness,
    Stage,
    get_llm,
    load_config,
)

from .prompts import (
    CLASS_ID_PROMPT,
    COMMON_LAW_PROMPT,
    FEDERAL_TESS_PROMPT,
    STATE_TM_PROMPT,
    SYNTHESIZER_PROMPT,
)
from .tools import all_tools


def _branches() -> list[Stage]:
    return [
        Stage(
            name="Federal TESS",
            system_prompt=FEDERAL_TESS_PROMPT,
            input_template="Proposed mark + goods/services:\n\n{input}",
        ),
        Stage(
            name="State TM Registries",
            system_prompt=STATE_TM_PROMPT,
            input_template="Proposed mark + goods/services:\n\n{input}",
        ),
        Stage(
            name="Common-Law Scan",
            system_prompt=COMMON_LAW_PROMPT,
            input_template="Proposed mark + goods/services:\n\n{input}",
        ),
        Stage(
            name="Class ID",
            system_prompt=CLASS_ID_PROMPT,
            input_template="Proposed mark + goods/services:\n\n{input}",
        ),
    ]


def _synthesizer() -> Stage:
    return Stage(
        name="Trademark Strategy Synthesis",
        system_prompt=SYNTHESIZER_PROMPT,
        tools=all_tools(),
        input_template=(
            "Findings from the four research branches:\n\n{input}\n\n"
            "Use these findings to produce the verdict + fee estimate + "
            "TEAS pre-fill + next steps. Call `uspto_fee_estimate` before "
            "writing the fee section."
        ),
    )


async def run(mark_and_goods: str, on_stage_complete=None) -> HarnessResult:
    """Run the parallel trademark research + synthesis.

    Args:
        mark_and_goods: Free text describing the proposed trademark and
            the founder's goods/services. Example: "Proposed mark:
            'BLUEHORSE'. Goods/services: AI-powered photo editing
            software for mobile devices (SaaS + downloadable iOS app).
            Founder is a CA LLC; primary market is US consumers."
        on_stage_complete: Optional callback `(stage_name, output)`
            invoked after each branch and the synthesizer — use to stream
            progress to a UI. Branch callbacks may fire in any order.

    Returns:
        HarnessResult. `final` is the synthesizer's markdown output (the
        report the founder reads); `stages` is the list of
        (branch_name, output) tuples for all five stages.
    """
    config = load_config(__file__)
    llm = get_llm(config)
    harness = ParallelHarness(
        llm=llm,
        branches=_branches(),
        synthesizer=_synthesizer(),
    )
    return await harness.run(mark_and_goods, on_stage_complete=on_stage_complete)


async def run_text(mark_and_goods: str) -> str:
    """Convenience: run and return the synthesizer's final report as a string."""
    result = await run(mark_and_goods)
    return result.final


if __name__ == "__main__":
    import sys
    default = (
        "Proposed mark: 'BLUEHORSE'. Goods/services: AI-powered photo "
        "editing software for mobile devices — both a downloadable iOS "
        "app and a web SaaS. Founder is a California LLC. Primary market "
        "is US consumers. Not yet used in commerce — planning to file "
        "intent-to-use."
    )
    user_input = " ".join(sys.argv[1:]) or default

    def progress(name, output):
        print(f"\n{'='*70}\n  Stage complete: {name}\n{'='*70}")
        print(output[:500] + ("..." if len(output) > 500 else ""))

    result = asyncio.run(run(user_input, on_stage_complete=progress))
    print("\n\n" + "=" * 70)
    print("  FINAL TRADEMARK STRATEGY REPORT")
    print("=" * 70)
    print(result.final)
