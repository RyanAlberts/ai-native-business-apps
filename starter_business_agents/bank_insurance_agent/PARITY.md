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
| g1 | 2-person SaaS for clinics, CA, no PHI | not yet run | — | — |
| g2 | Solo food truck operator in FL | not yet run | — | — |
| g3 | E-commerce skincare LLC, $400k rev | not yet run | — | — |
| g4 | Construction subcontractor in TX with 3 employees | not yet run | — | — |
| g5 | Pre-revenue solo consultant in NY | not yet run | — | — |

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
| claude | **verified by build smoke test** |
| openai | working (untested) |
| gemini | working (untested) |
| xai | community-supported |
| ollama | community-supported |
| codex | stub |
