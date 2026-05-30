# Parity Report — Loan & Funding Application Agent

| | |
|---|---|
| Path | `starter_business_agents/loan_application_agent/` |
| Default model | claude-sonnet-4-6 |
| Last verified | 2026-05-30 (full 5-case set captured live after the BOI-pitfall correctness pass) |

## 1. Capability parity (tools × providers)

No tools used in v1 — pure LLM reasoning. Trivially complete across providers.
For real-time SBA rate verification, enable `WebSearch` in
`config.yaml::allowed_tools` (Claude-only built-in).

| Tool | claude | openai | gemini | xai | ollama | codex |
|---|---|---|---|---|---|---|
| (none) | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ |

## 2. Behavioral parity (golden prompts)

| ID | Prompt | claude | openai | gemini |
|---|---|---|---|---|
| g1 | 2-yr LLC bakery, $280k rev, $120k for equipment | ✅ baselined 2026-05-30 | not run | not run |
| g2 | Pre-revenue solo SaaS founder, $30k for tooling | ✅ baselined 2026-05-30 | not run | not run |
| g3 | Restaurant in NYC, $500k for real estate | ✅ baselined 2026-05-30 | not run | not run |
| g4 | Veteran-owned landscaping, rural NC, $40k equipment | ✅ baselined 2026-05-30 | not run | not run |
| g5 | E-commerce skincare LLC (DE), $250k working capital | ✅ baselined 2026-05-30 | not run | not run |

Baseline: `tests/baselines/claude-2026-05-30.md` (full 5-case set),
captured live after the "missing the BOI deadline" pitfall was removed
(US-formed entities are exempt under the 2025 rule). Re-capture via `python
scripts/parity_run.py starter_business_agents.loan_application_agent`.

## 3. UX parity (Streamlit)

- [x] 2-column input form (business/state/stage | need/purpose/credit)
- [x] Free-text additional context
- [x] Primary action button
- [x] Markdown output + download

## 4. Known gaps

- Doesn't verify current rates or eligibility caps in real time without
  `WebSearch`.
- No fact-check against SBA's lender match tool (sba.gov/lendermatch).
- State-specific grant catalog depends on training data.

## 5. Verdict

| Provider | Verdict |
|---|---|
| claude | **verified by build smoke test** |
| openai | **working** (untested; no tools used) |
| gemini | **working** (untested; no tools used) |
| xai | community-supported |
| ollama | community-supported |
| codex | stub |
