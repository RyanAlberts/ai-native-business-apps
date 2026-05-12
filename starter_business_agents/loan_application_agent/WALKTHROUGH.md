# Walkthrough — Loan & Funding Application Agent

> "I need $120k to buy a second oven for my bakery. Where do I even start?
> SBA? Bank loan? Some grant I've never heard of?"

This agent gets a founder from "I need money" to "here's the program I'm
applying to first and here's what I need to gather." 90 seconds.

## What you'll see

Run `agent loan --cli "Two-year LLC bakery in Boise, $280k revenue, need $120k for equipment, founder credit 720, owns home with $120k equity"` and you'll get markdown with:

1. **Recommendation summary** — top 1–2 programs and why, plain English.
2. **Funding need analysis** — is $120k right-sized? Right kind of capital?
3. **Matched programs (ranked)** — typically SBA 7(a) and 504 for this
   profile, plus a microloan as a fallback. Each with fit rating.
4. **Readiness check** — concrete items (tax returns, P&L, SBA Form 413,
   articles/EIN), each marked ✅ / ⚠️ / ❌ based on what the founder
   described.
5. **Application package outline** — the exhibits in submission order.
6. **Order of operations** — this week, this month, this quarter.
7. **Pitfalls** — e.g. don't apply to 5 programs at once; lock in the SBA
   lender's preferred forms before requesting tax transcripts.
8. **Disclaimer** — pointer to sba.gov/local-assistance.

## How it works

One LLM call. No tools. The prompt does the work — it forces the model
to rank programs honestly, mark readiness items based on what the founder
disclosed, and sequence the action plan instead of dumping every option.

## Customizing it

- **Tweak the program list** — edit `SYSTEM_PROMPT` in `prompts.py` to
  emphasize state-specific programs (e.g. add California IBank Loan
  Guarantee Program, Massachusetts Growth Capital Corporation, etc.) or
  exclude programs that don't apply to your niche.
- **Get current rates** — enable `WebSearch` in `config.yaml::allowed_tools`.
  Now the agent can cite the current SBA 7(a) rate cap (Prime + 2.75% on
  loans > $50k, etc.) instead of ranges.
- **Swap to OpenAI** — `provider: openai` + `model: gpt-4o` in
  `config.yaml`, set `OPENAI_API_KEY`. The same prompt produces
  comparable output (slightly less specific without web access).

## Going further

- Pair with the [**Incorporation Agent**](../incorporation_agent/) — if
  the founder isn't yet incorporated, SBA loans require it.
- Pair with the [**Legal Document Generator**](../legal_doc_agent/) for
  operating agreements and personal-guarantee disclosures often required
  in the loan package.
- The output is a great input for a fundraising-specific Business Plan
  Implementation Manager run (just paste the founding-team summary + this
  plan as context).

## Footer

From **AI-Native Business Apps** — hand-built, provider-agnostic,
Apache-2.0. Built for founders who want AI baked in from day 0.
