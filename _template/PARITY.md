# Parity Report — Business Idea Validator (template)

| | |
|---|---|
| Source | Original work — template only, not in any folder yet |
| Default model | claude-sonnet-4-6 |
| Last verified | 2026-05-12 |

## 1. Capability parity (tools × providers)

This template uses no tools — the LLM reasons over plain text input.
Every provider supports text-only completion, so capability is trivially
complete across the board.

| Tool | claude | openai | gemini | xai | ollama | codex |
|---|---|---|---|---|---|---|
| (none) | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ stub |

## 2. Behavioral parity (golden prompts)

See `tests/golden.jsonl` (5 prompts spanning consumer SaaS, B2B, hardware,
marketplace, regulated).

| ID | Prompt | claude | openai | gemini |
|---|---|---|---|---|
| g1 | "An AI-powered shopping list app for busy parents." | verified | working | working |
| g2 | "Vertical SaaS for indie auto-body shops." | verified | working | working |
| g3 | "A connected hardware doorbell that detects packages." | verified | working | working |
| g4 | "A two-sided marketplace for freelance air-traffic controllers." | verified | working | working |
| g5 | "An online compounding pharmacy for ADHD medication." | verified | working | working |

Run captures live in `tests/runs/`.

## 3. UX parity (Streamlit)

- [x] Single input field (textarea, 120px)
- [x] Single button ("Validate idea")
- [x] Output as markdown
- [x] Download button

## 4. Cost / latency (informational only)

| Provider | Median latency | Notes |
|---|---|---|
| claude (subscription) | ~12s | Free under Max subscription |
| openai gpt-4o | ~8s | API billed, ~$0.01/run |

## 5. Known gaps

None for the template. (It's deliberately simple.)

## 6. Verdict

| Provider | Verdict |
|---|---|
| claude | **verified** |
| openai | **working** |
| gemini | **working** |
| xai | **community-supported** |
| ollama | **community-supported** |
| codex | **stub** |
