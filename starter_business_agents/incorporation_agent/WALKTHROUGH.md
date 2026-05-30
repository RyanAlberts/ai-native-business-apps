# Walkthrough — Incorporation Agent

> "I just decided to start a company. Should I form an LLC or an Inc.? Texas
> or Delaware? Do I need a lawyer for this?" — every solo founder, week 1.

This agent's job is to answer that question in 60 seconds with output that
isn't generic cargo-cult advice from a YC post.

## What you'll see

Paste this into the Streamlit UI:

> *Solo founder in Florida. Consulting business for local restaurants. $60k
> revenue expected year 1. No employees. No investors. Concerned about
> liability when clients act on my advice.*

The agent returns a markdown plan with:

1. **Recommendation summary** — leading with the decision, not the analysis.
   "Form a single-member LLC in Florida" — one sentence.
2. **Entity type** — why LLC vs S-Corp vs C-Corp for *this* founder.
3. **State of formation** — Florida (not the cargo-cult Delaware answer).
4. **Filing checklist** — 10 concrete steps with URLs (sunbiz.org, irs.gov/EIN)
   and dollar amounts (~$125 Articles, free EIN, etc.), including a check on
   FinCEN BOI status (US-formed entities are exempt under the 2025 rule).
5. **Registered agent options** — 3 services with costs, plus "act as your own"
   if applicable.
6. **Estimated costs table** — total range, line by line.
7. **Pitfalls specific to this founder** — commingling funds, no client
   agreement, BOI confusion (US-formed entities are now exempt), skipping
   E&O insurance.
8. **Disclaimer** — not legal advice.

## How it works

```
┌──────────────┐    ┌──────────────────────┐    ┌──────────────┐
│  app.py      │    │  agent.py            │    │  prompts.py  │
│  Streamlit   │ ─> │  run(founder_desc)   │ ─> │  SYSTEM_     │
│  UI form     │    │  load config + LLM   │    │  PROMPT      │
└──────────────┘    └──────────────────────┘    └──────────────┘
                            │
                            v
                    ┌──────────────────┐
                    │  core.LLMClient  │
                    │  (Claude default)│
                    └──────────────────┘
```

One LLM call. No tools. No loops. The intelligence is entirely in the
system prompt's structure — see `prompts.py::SYSTEM_PROMPT` for the eight
mandatory sections and the rules about defaulting to the simplest viable
structure.

The prompt's two most important rules:

1. **Default to the simplest viable structure.** Only recommend C-Corp when
   there's a real reason (priced VC round in 18 months, equity for many
   employees, etc.). Most founders are told to form Delaware C-Corps when an
   LLC in their home state would be far better.
2. **Never recommend a tax election as fact.** Say "discuss with your CPA
   whether to elect..." because state tax situations vary.

## Customizing it

### Add state-specific filing-fee lookup

The agent uses training-data filing fees ("approximate $125 in Florida"). For
current verified fees, enable Claude's built-in `WebSearch`:

```yaml
# config.yaml
allowed_tools:
  - WebSearch
```

Now the model can search current fees mid-response. (OpenAI/Gemini don't have
built-in web search; for those you'd add a `web_search` `Tool` in `tools.py`
that wraps SerpAPI or Tavily.)

### Change the tone

Edit `prompts.py::SYSTEM_PROMPT`. Replace the lead paragraph to make it
warmer / more formal / more skeptical. Don't touch the eight section headers
— the Streamlit UI assumes the structured output.

### Switch providers

For an OpenAI run with cost guarantees:

```yaml
provider: openai
model: gpt-4o
auth_mode: api_key
```

Set `OPENAI_API_KEY` in `.env` and re-run. Same code, different bill.

## Going further

- Pair this with the [**Legal Document Generator**](../) (Wave 3) to also
  draft the operating agreement and contractor agreements right after
  incorporation.
- Pair with the [**Bank & Insurance Setup Agent**](../) (Wave 3) so the
  founder finishes incorporation with a bank account and E&O policy quoted.
- Use the [**Business Plan Implementation Manager**](../../advanced_business_agents/multi_agent_apps/business_plan_implementation_manager/)
  *before* incorporation to validate whether you even should incorporate yet.

## Footer

From **AI-Native Business Apps** — hand-built, provider-agnostic, Apache-2.0.
A toolkit for founders who want AI baked in from day 0.
