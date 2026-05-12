# Parity Report — Business Plan Implementation Manager

| | |
|---|---|
| Path | `advanced_business_agents/multi_agent_apps/business_plan_implementation_manager/` |
| Default model | claude-sonnet-4-6 |
| Pattern | SequentialHarness, 4 stages |
| Last verified | 2026-05-12 |

## 1. Capability parity (tools × providers)

The pipeline's value depends most on the Market Research stage's access to
current data via web search. Claude has a built-in `WebSearch` tool; other
providers don't, so they fall back to training-data reasoning for stage 1.

| Tool / capability | claude | openai | gemini | xai | ollama | codex |
|---|---|---|---|---|---|---|
| WebSearch (built-in) | ✅ | ❌ (would need custom Tool) | ❌ (would need custom Tool) | ❌ | ❌ | ⏳ |
| Sequential orchestration | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ |
| Multi-stage tool routing | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ |

To bring other providers to full parity, add a `web_search` `Tool` in
`tools.py` wrapping SerpAPI / Tavily / Firecrawl. That's a 20-line change
and works across all providers via our abstraction.

## 2. Behavioral parity (golden prompts)

See `tests/golden.jsonl`.

| ID | Prompt | claude | openai | gemini |
|---|---|---|---|---|
| g1 | Vertical CRM for independent insurance brokers (2–10 employees) | **verified** (manual e2e during build; saved in `tests/baselines/claude-2026-05-12.md`) | not run | not run |
| g2 | Subscription box of locally-roasted coffee from cafes | not run | not run | not run |
| g3 | B2B service handling employer-side immigration paperwork | not run | not run | not run |

For verified runs, see baseline files in `tests/baselines/`.

## 3. UX parity (Streamlit)

- [x] Multi-field input form (idea, target market, founder background, budget)
- [x] Form submission (single primary button)
- [x] Progressive stage-by-stage output (expanders, one per stage)
- [x] Final roadmap expander expanded by default
- [x] Download button for combined plan markdown

## 4. Cost / latency (informational only)

| Provider | Median latency | Notes |
|---|---|---|
| claude (subscription + WebSearch) | ~120s | Free under Max; web search adds 10–30s |
| claude (subscription, no WebSearch) | ~80s | Same quality on stage 1 if model has good training data |
| openai gpt-4o | ~60s (est.) | ~$0.20–0.40/run, no web search in stage 1 |

## 5. Known gaps

- Stage 1 web search is Claude-only in v1. Other providers see degraded market
  research depth.
- No fact-check pass — model-cited numbers are not independently verified
  beyond the web-search results.
- No human-in-the-loop between stages. If stage 2's SWOT misreads the research,
  the rest of the pipeline compounds the error. (Per-stage callback hooks exist
  for the UI, but no edit-and-resume yet.)

## 6. Verdict

| Provider | Verdict |
|---|---|
| claude | **verified** with WebSearch enabled |
| openai | **working** (no web search in stage 1; quality of market research drops) |
| gemini | **working** (same caveat) |
| xai | **community-supported** |
| ollama | **community-supported** — needs a large local model (32B+) for usable output |
| codex | **stub** |
