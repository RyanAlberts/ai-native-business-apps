# 🏛️ Incorporation Agent

> Recommend an entity type, state of formation, registered agent, and filing
> checklist — tailored to the founder's specific situation. Not legal advice.

## What it does

Takes a free-text founder description (business idea, home state, cofounder
count, funding plans, hiring plans, liability concerns) and returns a markdown
recommendation with:

- Prominent disclaimer at the TOP (not buried at the bottom)
- Entity type pick (LLC / S-Corp election / C-Corp / Sole Prop / Partnership)
- State of formation (defaults to home state; recommends Delaware/Wyoming only
  when there's a real reason)
- Numbered 5–10 step filing checklist with EMBEDDED state-specific portal URLs
- Key documents & artifacts table — what to file, definitions, trade-offs,
  and follow-up questions the founder can paste back into the agent to drill
  down (e.g. "Draft me an Operating Agreement clause for unanimous consent")
- Expanded registered-agent options across three categories (act as your own
  RA, traditional services like Northwest / LegalZoom / Harbor Compliance,
  digital-first services like Doola / Stripe Atlas / Bizee) with a
  comparison table
- Estimated total cost table grounded in state-specific data
- Pitfalls specific to the founder's situation
- Business name availability check — if the founder proposes a specific
  name, the agent surfaces the official Secretary of State name-search URL
  for verification (no scraping; the founder does the lookup)

## Data sources

- `state_portals.py` — hand-curated portal URLs, filing fees, and notes for
  all 50 states + DC, plus federal links (IRS EIN, FinCEN BOI, USPTO
  trademark search). Single source of truth — update there and every Tool
  and prompt picks up the change.

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
