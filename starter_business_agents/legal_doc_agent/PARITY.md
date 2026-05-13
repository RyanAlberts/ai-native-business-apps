# Parity Report — Legal Document Generator

| | |
|---|---|
| Path | `starter_business_agents/legal_doc_agent/` |
| Default model | claude-sonnet-4-6 |
| Last verified | 2026-05-12 |

## 1. Capability parity (tools × providers)

| Tool | claude | openai | gemini | xai | ollama | codex |
|---|---|---|---|---|---|---|
| (none) | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ |

## 2. Behavioral parity (golden prompts)

| ID | Prompt | claude | openai | gemini |
|---|---|---|---|---|
| g1 | Mutual NDA, DE LLC <> NY Inc., 2-yr term | ✅ verified | not run | not run |
| g2 | Single-member LLC Operating Agreement, Wyoming | ✅ verified | not run | not run |
| g3 | Independent Contractor Agreement for a CA designer | ✅ verified | not run | not run |
| g4 | Privacy Policy for a US SaaS handling EU users | ✅ verified | not run | not run |
| g5 | Cofounder Agreement / 50-50 equity split memo | ✅ verified | not run | not run |

Claude baseline at `tests/baselines/claude-2026-05-12.md` (~118KB; 5 cases). Re-run with `python scripts/parity_run.py starter_business_agents.legal_doc_agent` — output goes to `tests/runs/` (gitignored) for diff against the baseline.

## 3. UX parity (Streamlit)

- [x] Document type dropdown
- [x] Party A / Party B inputs
- [x] State of formation + operation
- [x] Specifics free-text
- [x] Markdown output + download

## 4. Known gaps

- No PDF export (markdown only). Users can paste into a document editor.
- No state law database — leans on training-data knowledge.
- No version control between drafts (each run is independent).
- Industry-specific rule detection (HIPAA, COPPA, etc.) depends on whether
  the founder mentions the industry in the request.

## 5. Verdict

| Provider | Verdict |
|---|---|
| claude | **verified** — full 5-prompt golden run captured |
| openai | **working** (untested) |
| gemini | **working** (untested) |
| xai | community-supported |
| ollama | community-supported (large model recommended) |
| codex | stub |

**Note:** All output should be reviewed by a licensed attorney. The agent
explicitly outputs a disclaimer to this effect.
