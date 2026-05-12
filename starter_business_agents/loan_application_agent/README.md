# 💰 Loan & Funding Application Agent

> Match a small business to SBA loans, microloans, grants, and CDFI programs.
> Returns a ranked list of programs, an application readiness checklist, and
> a recommended order of operations. Not financial advice.

## What it does

Takes a founder's business + funding need (amount, purpose, stage, credit,
collateral) and returns:

- Top 3–5 matched programs (SBA 7(a) / 504 / Microloan, state grants,
  USDA Rural, CDC microloans, CDFIs) with fit rating + reasoning
- Readiness checklist marked ✅ / ⚠️ / ❌
- Application package outline (which exhibits, in what order)
- Recommended order of operations (this week / month / quarter)
- Founder-specific pitfalls

## Run

```bash
agent loan                              # Streamlit UI
agent loan --cli "Two-year LLC bakery in Boise, need $120k for an oven."
```

## Customize

- **Prompt** — `prompts.py::SYSTEM_PROMPT`. Adjust the section structure
  or tone.
- **Provider / model** — `config.yaml::provider`.
- **Add current-rate verification** — enable `WebSearch` in
  `config.yaml::allowed_tools` (Claude built-in) so the agent can cite
  current SBA rates rather than ranges.

## Provider parity

Verified on Claude (subscription). OpenAI/Gemini work; Ollama
community-supported. See [PARITY.md](./PARITY.md).
