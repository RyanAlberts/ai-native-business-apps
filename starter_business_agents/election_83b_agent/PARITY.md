# Parity Report — 83(b) Election Agent

| | |
|---|---|
| Source | Original work (motivated by Stripe Atlas's Auto-83(b) being closed-source and formation-bundled) |
| Default model | claude-sonnet-4-6 |
| Last verified | not yet run end-to-end |

## 1. Capability parity (tools × providers)

Two deterministic tools, pure-Python — no network, no provider-specific
features. Every provider that supports tool use can run this agent.

| Tool | claude | openai | gemini | xai | ollama | codex |
|---|---|---|---|---|---|---|
| `eighty_three_b_deadline_check` | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ stub |
| `irs_service_center_for_state` | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ stub |

## 2. Behavioral parity (golden prompts)

See `tests/golden.jsonl`.

| ID | Scenario | claude | openai | gemini |
|---|---|---|---|---|
| g1 | Solo founder, fresh DE C-Corp, FMV == price paid, ~25 days remaining | not yet run | not yet run | not yet run |
| g2 | Married-filing-jointly cofounder pair, vesting acceleration on change of control | not yet run | not yet run | not yet run |
| g3 | Grant 22 days ago — urgent (`NEAR` window) | not yet run | not yet run | not yet run |
| g4 | Grant 45 days ago — `EXPIRED`; agent must recommend §9100 path | not yet run | not yet run | not yet run |
| g5 | Non-US founder with ITIN — flag complexity, recommend specialized advice | not yet run | not yet run | not yet run |

## 3. UX parity (Streamlit)

- [x] Form-based input (not free text) — easier for founders who don't want to type structured prose
- [x] Date picker for grant date (prevents ISO-format mistakes)
- [x] State of residence dropdown (drives the IRS center lookup)
- [x] Single "Prepare 83(b)" submit button
- [x] Markdown output + full download

## 4. Cost / latency (informational only)

Expected. Tool calls are pure Python (≤1 ms each); the LLM does the
formatting work. Two short tool turns + one final response, so this
should be lighter than agents that emit longer narratives.

## 5. Known gaps

- **No PDF output yet** — the letter is markdown / plain text. Founders
  paste it into a Word doc and print. A PDF generation step would be a
  natural follow-up (e.g. `weasyprint` or `reportlab`).
- **No e-signature integration** — the IRS still typically requires a wet
  signature; Form 15620 e-file is offered as an alternative.
- **IRS service-center table is a snapshot** — when the IRS reroutes
  centers, this file needs updating. The agent always links the IRS
  lookup URL so a stale snapshot won't silently mislead a founder, but
  the snapshot itself needs an annual review.
- **No §9100 relief workflow** — if the deadline has passed, the agent
  refers to a tax attorney. Building out a §9100 letter generator would
  be a deeper follow-up.
- **No multi-grant batching** — a founder receiving stock at incorporation
  AND a separate option grant 90 days later needs two separate 83(b)
  filings; the agent handles one at a time.

## 6. Verdict

| Provider | Verdict |
|---|---|
| claude | not yet verified (scaffold only — needs end-to-end run) |
| openai | not yet run |
| gemini | not yet run |
| xai | community-supported |
| ollama | community-supported |
| codex | stub |
