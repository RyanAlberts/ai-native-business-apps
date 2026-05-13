# Parity Report — Supplier Sourcing Team

| | |
|---|---|
| Path | `advanced_business_agents/multi_agent_apps/supplier_sourcing_team/` |
| Default model | claude-sonnet-4-6 |
| Pattern | SequentialHarness, 4 stages |
| Last verified | 2026-05-12 |

## 1. Capability parity

Stage 1 (sourcing) materially benefits from `WebSearch` for naming real
suppliers. Other stages work equally on all providers.

| Capability | claude | openai | gemini | xai | ollama | codex |
|---|---|---|---|---|---|---|
| Sequential orchestration | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ |
| Real-supplier sourcing (WebSearch) | ✅ | ❌ (needs custom Tool) | ❌ | ❌ | ❌ | ⏳ |
| Generic sourcing (categories + directories) | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ |

## 2. Behavioral parity

| ID | Prompt | claude | openai | gemini |
|---|---|---|---|---|
| g1 | Silicone kitchenware contract manufacturer | ✅ verified | — | — |
| g2 | Boutique design agency for SaaS brand redesign | ✅ verified | — | — |
| g3 | Wholesale roasted coffee for office subscription | ✅ verified | — | — |

Claude baseline at `tests/baselines/claude-2026-05-12.md` (~348KB; 3 cases × 4 stages, WebSearch enabled). Re-run with `python scripts/parity_run.py advanced_business_agents.multi_agent_apps.supplier_sourcing_team`.

## 3. UX parity

- [x] Multi-field form (need / volume / budget / quality / timeline / geo)
- [x] Progressive stage-by-stage Streamlit output
- [x] Comparison matrix expander expanded by default
- [x] Combined download

## 4. Known gaps

- Stage 1 supplier names are best-effort; always verify with WebSearch +
  direct contact before relying.
- No automatic price-benchmark scraping.
- No integration with Alibaba / Thomasnet APIs (community-supported, not
  in v1).
- Vetting rubric weights are defaults — adjust per category.

## 5. Verdict

| Provider | Verdict |
|---|---|
| claude (with WebSearch) | **verified** — full 3-prompt × 4-stage golden run captured |
| claude (no WebSearch) | working — degraded sourcing stage |
| openai | working (degraded sourcing) |
| gemini | working (degraded sourcing) |
| xai | community-supported |
| ollama | community-supported |
| codex | stub |
