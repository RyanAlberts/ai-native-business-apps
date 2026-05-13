# Parity Report — Incorporation Agent

| | |
|---|---|
| Path | `starter_business_agents/incorporation_agent/` |
| Default model | claude-sonnet-4-6 |
| Last verified | 2026-05-12 (post-feedback rev) |

## 1. Capability parity (tools × providers)

The agent uses two deterministic, no-network tools (defined in `tools.py`,
data in `state_portals.py`). Both work uniformly across providers because
they're handled in our adapter layer — every provider routes tool calls
through `core.Tool`, just via different native SDK shapes.

| Tool | claude | openai | gemini | xai | ollama | codex |
|---|---|---|---|---|---|---|
| `state_business_name_search` | ✅ | ✅ (untested) | ✅ (untested) | ✅ | ✅ | ⏳ stub |
| `state_portal_lookup` | ✅ | ✅ (untested) | ✅ (untested) | ✅ | ✅ | ⏳ stub |

Optionally enabling `WebSearch` in `config.yaml::allowed_tools` adds
live-data verification of filing fees; that's Claude-only.

## 2. Behavioral parity (golden prompts)

See `tests/golden.jsonl`.

| ID | Prompt | claude | openai | gemini |
|---|---|---|---|---|
| g1 | Solo founder TX, bootstrapped SaaS, no VC | ✅ verified (build smoke) | not run | not run |
| g2 | 2 cofounders CA, seed in 9mo, fintech | not run | not run | not run |
| g3 | Solo FL, restaurant consultant, $80k yr | ✅ verified (manual) | not run | not run |
| g4 | 3 cofounders NY, AI hardware, $200k pre-seed | not run | not run | not run |
| g5 | Solo WY, drop-shipping, product liability | not run | not run | not run |

Baseline captures:
- `tests/baselines/claude-2026-05-12-smoke.md` — Texas SaaS w/ "Acme Books"
  name; verifies the new tools (state portal lookup + name-search URL) fire
  end-to-end, disclaimer is at top, Key Documents & Artifacts table renders,
  RA section covers all three categories incl. LegalZoom.

To run the full 5-prompt sweep:
`python scripts/parity_run.py starter_business_agents.incorporation_agent`

## 3. UX parity (Streamlit)

- [x] 2-column input layout (business name, state, cofounders | funding, hiring)
- [x] Free-text description box
- [x] Single primary button
- [x] Output rendered as markdown
- [x] Download button for the plan

## 4. Cost / latency (informational only)

| Provider | Median latency | Notes |
|---|---|---|
| claude (subscription) | ~25s with two tool calls | Free under Max |
| openai gpt-4o | ~15s (est.) | Not measured; ~$0.03/run with tool calls |

## 5. Known gaps

- State portal URLs in `state_portals.py` are best-effort as of repo write
  date. Some may have drifted; the data module is the single source of
  truth so any fix lands in one place.
- Filing fees are based on training data + the curated table; for current
  2026 fees, enable `WebSearch` (Claude only).
- No real-time RA-service price verification.
- No automatic state-of-operation foreign-LLC requirement detection beyond
  what the LLM infers from the founder description.

## 6. Verdict

| Provider | Verdict |
|---|---|
| claude | **verified** — tools fire, output structure matches spec |
| openai | **working** (untested) — tools should route through our manual loop |
| gemini | **working** (untested) — same |
| xai | **community-supported** |
| ollama | **community-supported** — quality depends on local model size |
| codex | **stub** |
