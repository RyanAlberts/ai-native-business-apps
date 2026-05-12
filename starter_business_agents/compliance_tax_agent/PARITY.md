# Parity Report — Compliance & Tax Setup Agent

| | |
|---|---|
| Path | `starter_business_agents/compliance_tax_agent/` |
| Default model | claude-sonnet-4-6 |
| Last verified | 2026-05-12 |

## 1. Capability parity

No tools used. All providers can produce the structured plan. Adding
`WebSearch` (Claude built-in) materially improves accuracy of current-year
nexus thresholds.

| Tool | claude | openai | gemini | xai | ollama | codex |
|---|---|---|---|---|---|---|
| (none) | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ |
| WebSearch (optional) | ✅ | ❌ (needs custom Tool) | ❌ | ❌ | ❌ | ⏳ |

## 2. Behavioral parity (golden prompts)

| ID | Prompt | claude | openai | gemini |
|---|---|---|---|---|
| g1 | DE LLC, CA operation, Shopify+Amazon skincare $200k | not yet run | — | — |
| g2 | TX S-Corp consulting, 3 employees, services only | not yet run | — | — |
| g3 | NY sole prop coaching, $80k yr 1, all customers in NY | not yet run | — | — |
| g4 | FL LLC food truck + catering, $300k, 2 employees | not yet run | — | — |
| g5 | DE C-Corp B2B SaaS, $1.2M, contractors only, no inventory | not yet run | — | — |

## 3. UX parity

- [x] Entity type dropdown
- [x] Multi-state input
- [x] Sales channels free-text
- [x] Markdown output + download

## 4. Known gaps

- Current-year nexus thresholds depend on training data without WebSearch.
- Local business licenses (city/county) are out of scope — agent flags
  the category but doesn't enumerate.
- Industry-specific compliance (FDA, FCC, FINRA, HIPAA) only triggers
  when the founder mentions the industry in the request.

## 5. Verdict

| Provider | Verdict |
|---|---|
| claude | **verified by build smoke test** |
| openai | working (untested) |
| gemini | working (untested) |
| xai | community-supported |
| ollama | community-supported |
| codex | stub |
