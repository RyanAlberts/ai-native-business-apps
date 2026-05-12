# Parity Report — Website Launch Team

| | |
|---|---|
| Path | `advanced_business_agents/multi_agent_apps/website_launch_team/` |
| Default model | claude-sonnet-4-6 |
| Pattern | SequentialHarness, 4 stages |
| Last verified | 2026-05-12 |

## 1. Capability parity

No tools used in v1. Stage 1 (naming + domain) benefits most from `WebSearch`
for availability sniff checks, but isn't required.

| Capability | claude | openai | gemini | xai | ollama | codex |
|---|---|---|---|---|---|---|
| Sequential orchestration | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ |
| Brand/naming quality | ✅ strong | working | working | community | community | ⏳ |

## 2. Behavioral parity

| ID | Prompt | claude | openai | gemini |
|---|---|---|---|---|
| g1 | AI hiring screener for SaaS recruiting | not yet run | — | — |
| g2 | Local coffee subscription box for offices | not yet run | — | — |
| g3 | B2B service for employer immigration paperwork | not yet run | — | — |

## 3. UX parity

- [x] Multi-field form input
- [x] Progressive stage-by-stage Streamlit output
- [x] Final checklist expander open by default
- [x] Combined download

## 4. Known gaps

- No real-time `.com` availability check — agent flags to verify at a
  registrar.
- No competitor visual scrape — visual direction is built from description
  + best practices, not from a competitor analysis pass.
- No actual logo generation — concept text only.
- No A/B test variant generation in copy stage.

## 5. Verdict

| Provider | Verdict |
|---|---|
| claude | **verified by build smoke test** |
| openai | working (untested) |
| gemini | working (untested) |
| xai | community-supported |
| ollama | community-supported (32B+ recommended) |
| codex | stub |
