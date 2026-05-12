# 🏛️ Incorporation Agent

> Recommend an entity type, state of formation, registered agent, and filing
> checklist — tailored to the founder's specific situation. Not legal advice.

## What it does

Takes a free-text founder description (business idea, home state, cofounder
count, funding plans, hiring plans, liability concerns) and returns a markdown
recommendation with:

- Entity type pick (LLC / S-Corp election / C-Corp / Sole Prop / Partnership)
- State of formation (defaults to home state; recommends Delaware/Wyoming only
  when there's a real reason)
- Numbered 5–10 step filing checklist
- 2–3 registered-agent options with cost ranges
- Estimated total cost table
- Pitfalls specific to the founder's situation
- Disclaimer (not legal advice; consult CPA/attorney)

## Run

From the repo root, with Claude Max logged in via `claude` CLI:

```bash
unset ANTHROPIC_API_KEY    # use subscription
streamlit run starter_business_agents/incorporation_agent/app.py
```

Or CLI:

```bash
python -m starter_business_agents.incorporation_agent.agent \
  "Solo founder in Texas. Bootstrapped SaaS for accounting firms."
```

## Customize

- **Tone / scope** — edit `prompts.py::SYSTEM_PROMPT`.
- **Provider / model** — edit `config.yaml::provider` (claude, openai, gemini, …).
- **Add web search** for real-time filing-fee verification — uncomment
  `WebSearch` in `config.yaml::allowed_tools` (Claude built-in). For other
  providers, define a custom Tool in `tools.py`.

## Why this is hard to get right

Founders often default to "Delaware C-Corp" because that's what they read in
YC posts. For a bootstrapped solo founder with no VC plans, a Delaware C-Corp
is usually wrong — double taxation, franchise tax, foreign-LLC registration
in their home state, complexity overhead. The agent's job is to push back on
the cargo-cult default and recommend the simplest viable structure.

## Provider parity

See [PARITY.md](./PARITY.md). Verified on Claude; OpenAI/Gemini working.

## Model

Claude Sonnet 4.6 (low temperature: 0.2). The advice should be deterministic.
