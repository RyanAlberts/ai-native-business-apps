# Parity Report — Bank & Insurance Setup Agent

| | |
|---|---|
| Path | `starter_business_agents/bank_insurance_agent/` |
| Default model | claude-sonnet-4-6 |
| Last verified | 2026-05-12 |

## 1. Capability parity

No tools used. All providers can produce the structured markdown.

| Tool | claude | openai | gemini | xai | ollama | codex |
|---|---|---|---|---|---|---|
| (none) | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ |

## 2. Behavioral parity (golden prompts)

| ID | Prompt | claude | openai | gemini |
|---|---|---|---|---|
| g1 | 2-person SaaS for clinics, CA, no PHI | ✅ verified | — | — |
| g2 | Solo food truck operator in FL | ✅ verified | — | — |
| g3 | E-commerce skincare LLC, $400k rev | ✅ verified | — | — |
| g4 | Construction subcontractor in TX with 3 employees | ✅ verified | — | — |
| g5 | Pre-revenue solo consultant in NY | ✅ verified | — | — |

Claude baseline at `tests/baselines/claude-2026-05-12.md` (~60KB; 5 cases). Re-run with `python scripts/parity_run.py starter_business_agents.bank_insurance_agent`.

## 3. UX parity

- [x] Multi-field form (business / state / stage / employees / physical / data)
- [x] Additional-context free-text
- [x] Markdown output + download

## 4. Known gaps

- Real-time premium quotes require carrier websites; the agent gives ranges
  only.
- State-specific workers' comp triggers depend on training data — verify
  for your state at the Department of Industrial Relations / Labor Bureau.
- No automatic detection of regulated industries beyond what's mentioned
  in the request.

## 5. Verdict

| Provider | Verdict |
|---|---|
| claude | **verified** — full 5-prompt golden run captured |
| openai | working (untested) |
| gemini | working (untested) |
| xai | community-supported |
| ollama | community-supported |
| codex | stub |
