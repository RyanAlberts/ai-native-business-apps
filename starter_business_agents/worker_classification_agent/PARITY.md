# Parity Report — Worker Classification Agent

| | |
|---|---|
| Source | Original work; IRS three-category test + DOL 2024 Final Rule + AB5/MA/NJ ABC tests |
| Default model | claude-sonnet-4-6 |
| Last verified | not yet run end-to-end |

## 1. Capability parity (tools × providers)

Two reference-data tools, pure-Python — every tool-capable provider works.

| Tool | claude | openai | gemini | xai | ollama | codex |
|---|---|---|---|---|---|---|
| `classification_tests_reference` | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ stub |
| `state_classification_law_lookup` | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ stub |

## 2. Behavioral parity (golden prompts)

See `tests/golden.jsonl`.

| ID | Scenario | claude | openai | gemini |
|---|---|---|---|---|
| g1 | CA "1099 engineer" in our office on our laptop — clear W-2 + AB5 fail | not yet run | not yet run | not yet run |
| g2 | Genuine 1099 case: out-of-state freelance designer with own equipment + other clients + flat-fee per project | not yet run | not yet run | not yet run |
| g3 | Borderline / HIGH RISK in NY: part-time bookkeeper, owns equipment, but only this one client and 30 hours/week | not yet run | not yet run | not yet run |
| g4 | TX (common-law state, no ABC) — full-time content writer, our equipment, our schedule. Federal says W-2. | not yet run | not yet run | not yet run |
| g5 | MA construction subcontractor — fails B prong (same trade as hiring entity) | not yet run | not yet run | not yet run |

## 3. UX parity (Streamlit)

- [x] Form-based input with structured selectors (not free text)
- [x] Boolean checkbox for "is role core to the business?" — the
      integral-to-business factor needs an explicit input
- [x] Single Classify button
- [x] Download analysis

## 4. Cost / latency

Two short tool calls + one final response. Expected fast and cheap —
the analytical work is in the prompt, not in iterative tool calls.

## 5. Known gaps

- **AB5 exemption lookup** — California's AB5 has dozens of industry-
  specific exemptions (lawyers, doctors, real estate agents, certain
  creative professionals, etc.). The agent flags when an exemption
  MIGHT apply but doesn't authoritatively determine it. Adding an AB5
  exemption checker would be a natural follow-up.
- **Dollar-penalty calculation** — the agent quantifies misclassification
  cost qualitatively but doesn't compute the exact back-tax owed
  (would require wage + tenure + state-by-state penalty tables).
- **No PEO/HRIS provider quotes** — the agent recommends Gusto/Rippling/
  Justworks/TriNet but doesn't quote prices for the founder's specific
  setup.
- **No contract drafting** — the agent points at `legal_doc_agent` for
  the actual contract. A future PR could chain them automatically.
- **State coverage**: explicit data for 5 states (CA, MA, NJ, IL, NY).
  All others fall through to federal default — accurate for most but
  misses state-specific quirks (e.g. CT unemployment ABC test; OR
  similar). Adding more state data is a low-friction follow-up.

## 6. Verdict

| Provider | Verdict |
|---|---|
| claude | not yet verified (scaffold only — needs end-to-end run) |
| openai | not yet run |
| gemini | not yet run |
| xai | community-supported |
| ollama | community-supported |
| codex | stub |
