# Parity Report — Delaware Franchise Tax Calculator

| | |
|---|---|
| Source | Original work; formulas from 8 Del. C. §§ 501-507 + Delaware Division of Corporations calculator |
| Default model | claude-sonnet-4-6 |
| Last verified | not yet run end-to-end |

## 1. Capability parity (tools × providers)

Two deterministic tools, pure-Python — no network, no provider-specific
features. Every tool-capable provider works.

| Tool | claude | openai | gemini | xai | ollama | codex |
|---|---|---|---|---|---|---|
| `delaware_franchise_tax_calc` | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ stub |
| `delaware_llc_flat_tax` | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ stub |

## 2. Behavioral parity (golden prompts)

See `tests/golden.jsonl`.

| ID | Scenario | claude | openai | gemini |
|---|---|---|---|---|
| g1 | Classic founder shock: 10M auth, 8M issued, par .0001, $50K assets → $85K default vs $400 APVC | not yet run | not yet run | not yet run |
| g2 | Later-stage with real assets: 10M auth, 10M issued, $10M assets → APVC still wins ($4K) | not yet run | not yet run | not yet run |
| g3 | Newly formed C-Corp, no issued shares yet → AUTH method beats APVC floor | not yet run | not yet run | not yet run |
| g4 | DE LLC, not a C-Corp — flat $300 | not yet run | not yet run | not yet run |
| g5 | Tiny par value but high authorized: 100M auth, 1M issued, par .00001, $20K assets | not yet run | not yet run | not yet run |

## 3. UX parity (Streamlit)

- [x] Entity-type toggle (C-Corp/LLC) — different math, different UI
- [x] Form inputs with sensible defaults for the founder scenario
- [x] Bill-amount input (optional) for context-aware response
- [x] Single submit button
- [x] Markdown output

## 4. Cost / latency

Expected to be fast — one tool call typical, short response. Lower
token use than 83(b) agent (no letter generation).

## 5. Known gaps

- **No DE portal automation** — DE's payment portal requires manual
  login + radio-button selection. Even with their API, the agent
  intentionally doesn't auto-pay (irreversible action).
- **No gross-assets reconciliation** — the agent trusts the founder's
  reported number. CPAs handle the books-to-Schedule-L mapping.
- **Single year only** — no multi-year planning (e.g. "if you authorize
  N shares now, here's your tax at hypothetical M assets next year").
- **No LP/GP-specific guidance** — they pay the same $300 flat as LLCs;
  the agent collapses them into one path.

## 6. Verdict

| Provider | Verdict |
|---|---|
| claude | not yet verified (scaffold only — needs end-to-end run) |
| openai | not yet run |
| gemini | not yet run |
| xai | community-supported |
| ollama | community-supported |
| codex | stub |
