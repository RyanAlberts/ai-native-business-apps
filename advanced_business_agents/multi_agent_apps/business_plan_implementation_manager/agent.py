# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Business Plan Implementation Manager — sequential 4-stage pipeline.

Inspired by Google ADK's SequentialAgent pattern; rebuilt provider-agnostically
on top of `core.SequentialHarness` so the same code runs against Claude, OpenAI,
Gemini, or Ollama by editing `config.yaml`.

Pipeline:
    1. Market Research   — gather context (web search if available)
    2. SWOT              — analyze the research
    3. Strategy          — pick objectives, segment, channel, price
    4. Roadmap           — 30/60/90-day execution plan
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass

from core import (
    HarnessResult,
    SequentialHarness,
    Stage,
    get_llm,
    load_config,
)

from .prompts import (
    MARKET_RESEARCH_PROMPT,
    ROADMAP_PROMPT,
    STRATEGY_PROMPT,
    SWOT_PROMPT,
)
from .tools import all_tools


def _stages() -> list[Stage]:
    tools = all_tools()
    return [
        Stage(name="Market Research", system_prompt=MARKET_RESEARCH_PROMPT, tools=tools),
        Stage(
            name="SWOT Analysis",
            system_prompt=SWOT_PROMPT,
            input_template="Market research brief:\n\n{input}",
        ),
        Stage(
            name="Strategy",
            system_prompt=STRATEGY_PROMPT,
            input_template="Preceding analysis:\n\n{input}",
        ),
        Stage(
            name="Implementation Roadmap",
            system_prompt=ROADMAP_PROMPT,
            input_template="Strategy:\n\n{input}",
        ),
    ]


async def run(business_idea: str, on_stage_complete=None) -> HarnessResult:
    """Run the full 4-stage pipeline.

    Args:
        business_idea: Free-text describing the business idea and any context
            (target market, founder background, budget, timing).
        on_stage_complete: Optional callback `(stage_name, output)` invoked
            after each stage — use to stream intermediate results to a UI.

    Returns:
        HarnessResult with `final` (the roadmap markdown) and `stages`
        (list of `(stage_name, output)` tuples for the four stages).
    """
    config = load_config(__file__)
    llm = get_llm(config)
    harness = SequentialHarness(llm=llm, stages=_stages())
    return await harness.run(business_idea, on_stage_complete=on_stage_complete)


async def run_text(business_idea: str) -> str:
    """Convenience: run the full pipeline and return a single combined markdown."""
    result = await run(business_idea)
    sections = [f"# {name}\n\n{output}" for name, output in result.stages]
    return "\n\n---\n\n".join(sections)


if __name__ == "__main__":
    import sys
    default = (
        "I'm a former enterprise SaaS sales rep. I want to build a vertical "
        "CRM specifically for independent insurance brokers. Target market: "
        "the ~36k US brokerages with 2-10 employees. I have $50k savings to "
        "fund 6 months of focused work."
    )
    idea = " ".join(sys.argv[1:]) or default

    def progress(name, output):
        print(f"\n{'='*70}\n  Stage complete: {name}\n{'='*70}")
        print(output[:500] + ("..." if len(output) > 500 else ""))

    result = asyncio.run(run(idea, on_stage_complete=progress))
    print("\n\n" + "=" * 70)
    print("  FINAL ROADMAP")
    print("=" * 70)
    print(result.final)
