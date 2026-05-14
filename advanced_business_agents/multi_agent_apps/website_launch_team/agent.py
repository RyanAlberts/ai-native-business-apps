# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Website Launch Team — sequential 4-stage pipeline.

Stage 1: Brand & Domain (name, voice, visual direction)
Stage 2: Site Architecture (sitemap, page outlines, tech stack)
Stage 3: Copy & Design Direction (hero, features, design brief)
Stage 4: Launch Checklist (DNS, QA, analytics, day-0 + 30-day plan)
"""
from __future__ import annotations

import asyncio

from core import HarnessResult, SequentialHarness, Stage, get_llm, load_config

from .prompts import (
    BRAND_DOMAIN_PROMPT,
    COPY_DESIGN_PROMPT,
    LAUNCH_CHECKLIST_PROMPT,
    SITE_ARCHITECTURE_PROMPT,
)
from .tools import all_tools


def _stages() -> list[Stage]:
    tools = all_tools()
    return [
        Stage(name="Brand & Domain", system_prompt=BRAND_DOMAIN_PROMPT, tools=tools),
        Stage(
            name="Site Architecture",
            system_prompt=SITE_ARCHITECTURE_PROMPT,
            input_template="Brand direction:\n\n{input}",
        ),
        Stage(
            name="Copy & Design",
            system_prompt=COPY_DESIGN_PROMPT,
            input_template="Brand + architecture:\n\n{input}",
        ),
        Stage(
            name="Launch Checklist",
            system_prompt=LAUNCH_CHECKLIST_PROMPT,
            input_template="Preceding stages:\n\n{input}",
        ),
    ]


async def run(business_description: str, on_stage_complete=None) -> HarnessResult:
    """Run the 4-stage website launch pipeline.

    Args:
        business_description: Free-text covering the business idea, target
            audience, founder background, budget, timeline.
        on_stage_complete: Optional callback `(stage_name, output)`.

    Returns:
        HarnessResult — `final` is the launch checklist; `stages` has all 4.
    """
    config = load_config(__file__)
    llm = get_llm(config)
    harness = SequentialHarness(llm=llm, stages=_stages())
    return await harness.run(business_description, on_stage_complete=on_stage_complete)


if __name__ == "__main__":
    import sys
    default = (
        "AI-powered hiring screener for SaaS recruiting teams. Target: "
        "talent acquisition leads at 50–500 person SaaS companies. Founder "
        "is a former recruiter turned engineer. Bootstrapped, $30k budget "
        "for site + initial marketing. Timeline: live in 14 days."
    )
    desc = " ".join(sys.argv[1:]) or default

    def progress(name: str, output: str) -> None:
        # flush=True so partial progress is visible if the run is killed.
        print(f"\n{'='*70}\n  Stage complete: {name}\n{'='*70}", flush=True)
        print(output[:400] + ("..." if len(output) > 400 else ""), flush=True)

    result = asyncio.run(run(desc, on_stage_complete=progress))
    print(f"\n{'='*70}\n  FINAL LAUNCH CHECKLIST\n{'='*70}")
    print(result.final)
