# 📋 Business Plan Implementation Manager

> A sequential 4-stage pipeline that turns a business idea into a 30/60/90-day
> execution roadmap. Market Research → SWOT → Strategy → Roadmap.

## What it does

Given a business idea (plus optional context: target market, founder background,
budget/runway), runs four LLM stages in sequence:

| # | Stage | What it produces |
|---|---|---|
| 1 | **Market Research** | Market overview, customer segments, competition, pricing landscape, recent shifts. Uses web search if available. |
| 2 | **SWOT Analysis** | SWOT quadrants grounded in the research brief, plus strategic implications. |
| 3 | **Strategy** | Strategic objectives (6 months), beachhead market, positioning statement, GTM channel, pricing, **what NOT to do**. |
| 4 | **Implementation Roadmap** | 30/60/90-day deliverables with acceptance criteria, key metrics dashboard, critical decision forks, owner & cadence. |

Each stage's output is the input to the next, so the final roadmap is grounded
in the original idea through three layers of strategic reasoning.

## Run

```bash
# From the repo root, with Claude Max logged in via `claude` CLI:
unset ANTHROPIC_API_KEY
streamlit run advanced_business_agents/multi_agent_apps/business_plan_implementation_manager/app.py
```

Or CLI:

```bash
python -m advanced_business_agents.multi_agent_apps.business_plan_implementation_manager.agent \
  "A vertical CRM for independent insurance brokers (2-10 employees)."
```

Pipeline takes ~8–10 minutes end-to-end on `claude-sonnet-4-6` with web
search (per-stage ~120–140s × 4 stages observed in 2026-05-14 verification
runs). Without web search, closer to ~5–6 minutes. Set client timeouts
≥ 600s if you're scripting against this agent.

## How it's built

Uses `core.SequentialHarness` to wire 4 `Stage` objects together. The harness
is provider-agnostic — same code runs against OpenAI or Gemini by swapping
`config.yaml::provider`. See the [harness source](../../../core/harness/sequential_harness.py).

```python
from core import SequentialHarness, Stage

stages = [
    Stage(name="Market Research", system_prompt=MARKET_RESEARCH_PROMPT, tools=[...]),
    Stage(name="SWOT Analysis",  system_prompt=SWOT_PROMPT,            input_template="Market research brief:\n\n{input}"),
    Stage(name="Strategy",       system_prompt=STRATEGY_PROMPT,        input_template="Preceding analysis:\n\n{input}"),
    Stage(name="Roadmap",        system_prompt=ROADMAP_PROMPT,         input_template="Strategy:\n\n{input}"),
]

result = await SequentialHarness(llm, stages).run(idea)
```

## Customize

- **Add or remove stages** — edit the `_stages()` list in `agent.py`. The harness
  accepts any number of stages.
- **Swap prompts** — every stage's system prompt lives in `prompts.py`.
- **Different tools per stage** — pass per-stage `tools=` when constructing each
  `Stage`. E.g. give the Market Research stage WebSearch + Firecrawl, but no
  tools to the strategy stage.
- **Run a parallel rather than sequential pipeline** — a `ParallelHarness` is
  planned for v1.1; for now, you can compose your own with `asyncio.gather`.

## Inspiration

The sequential pattern is inspired by Google ADK's `SequentialAgent` (see the
example in [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/ai_agent_framework_crash_course/google_adk_crash_course/9_multi_agent_patterns/9_1_sequential_agent)).
The pattern is the same; the implementation is original work — none of the
upstream code or prompts are used.

## Provider parity

See [PARITY.md](./PARITY.md). Verified on Claude with `WebSearch` enabled.
Other providers run but degrade to training-data-only reasoning in the market
research stage.

## Model

Claude Sonnet 4.6 by default. Higher max_tokens (6144) since later stages
produce long structured output. Override in `config.yaml`.
