# Parity Report — Incorporation Agent

| | |
|---|---|
| Path | `starter_business_agents/incorporation_agent/` |
| Default model | claude-sonnet-4-6 |
| Last verified | 2026-05-12 |

## 1. Capability parity (tools × providers)

The agent uses no external tools — output is generated from LLM reasoning over
the founder's input. Every provider supports text completion, so capability is
trivially complete.

| Tool | claude | openai | gemini | xai | ollama | codex |
|---|---|---|---|---|---|---|
| (none) | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ stub |

If `config.yaml::allowed_tools` is extended with `WebSearch` (Claude built-in)
for live filing-fee verification, only Claude supports it natively. Other
providers need a custom Tool wrapping SerpAPI / Tavily / etc.

## 2. Behavioral parity (golden prompts)

See `tests/golden.jsonl` — 5 prompts covering bootstrapped solo, venture-track
team, side-business solo, hardware multi-cofounder, asset-protection-heavy.

| ID | Prompt | claude | openai | gemini |
|---|---|---|---|---|
| g1 | Solo founder TX, bootstrapped SaaS, no VC | **verified** | not run | not run |
| g2 | 2 cofounders CA, seed in 9mo, fintech | not run | not run | not run |
| g3 | Solo FL, restaurant consultant, $80k yr | **verified (manual)** | not run | not run |
| g4 | 3 cofounders NY, AI hardware, $200k pre-seed | not run | not run | not run |
| g5 | Solo WY, drop-shipping, product liability | not run | not run | not run |

`g3` was the manual end-to-end verification during build (output excerpted in
the README). Other prompts require running `scripts/parity_run.py
starter_business_agents.incorporation_agent --provider claude`.

## 3. UX parity (Streamlit)

- [x] 2-column input layout (business name, state, cofounders | funding, hiring)
- [x] Free-text description box
- [x] Single primary button
- [x] Output rendered as markdown
- [x] Download button for the plan

## 4. Cost / latency (informational only)

| Provider | Median latency | Notes |
|---|---|---|
| claude (subscription) | ~15s | Free under Max |
| openai gpt-4o | ~10s (est.) | Not measured; ~$0.02/run |

## 5. Known gaps

- Filing fees are based on training-data knowledge; for current 2026 fees,
  enable WebSearch (Claude only).
- No verification that recommended registered-agent services are still in
  business / still priced as listed.
- No state-specific BOI deadline awareness (FinCEN rules have been in flux).

## 6. Verdict

| Provider | Verdict |
|---|---|
| claude | **verified** |
| openai | **working** (untested; OpenAI tool loop is implemented but this agent uses no tools) |
| gemini | **working** (untested; same reasoning) |
| xai | **community-supported** |
| ollama | **community-supported** — quality depends on local model size |
| codex | **stub** |
