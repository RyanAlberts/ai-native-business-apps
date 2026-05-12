# Walkthrough — Compliance & Tax Setup Agent

> "I'm selling skincare on Shopify and Amazon. Do I need to register for
> sales tax in 50 states? When do I have to file what?"

This agent answers that — without the panicked CPA call.

## What you'll see

Run `agent compliance-tax` for a DE LLC selling skincare from CA via Shopify
and Amazon FBA. You get:

1. **Recommendation summary** — usually "register for sales tax in 5–8
   states where you've hit economic nexus thresholds; let Amazon FBA
   handle their states as a marketplace facilitator; foreign-register your
   DE LLC in CA."
2. **Sales tax nexus analysis** — split into physical (CA 3PL), economic
   (states where >$100k or >200 transactions), and marketplace facilitator
   (Amazon handles most).
3. **State business registrations** — foreign-LLC, sales tax permits, SUI
   if hiring.
4. **Federal filings** — quarterly estimated taxes, annual 1065/1120-S,
   1099-NEC for contractors, BOI with FinCEN.
5. **State filings per state** — CA Statement of Information, DE franchise
   tax, sales tax returns per registered state.
6. **Bookkeeping setup** — usually QuickBooks Online for accountant
   compatibility.
7. **Advisor engagement plan** — when to hire a CPA vs a bookkeeper.
8. **30/60/90-day plan** with concrete deadlines.

## How it works

One LLM call, temperature 0.2. The prompt is structured to PREVENT the
common failure mode where the agent recommends every possible filing
"to be safe" — it ranks by necessity for THIS founder's specific profile
(e.g. no SUI section if there are no employees).

## Customizing it

### Add industry compliance rules

Edit `prompts.py::SYSTEM_PROMPT`. Insert: *"If business handles food,
include FDA registration (21 CFR §1.225) and state health department
permit."*

### Use WebSearch for current thresholds

```yaml
# config.yaml
allowed_tools:
  - WebSearch
```

The agent can now cite Massachusetts's $100k economic nexus threshold
verbatim instead of giving a range.

### Different revenue tiers

Edit the system prompt to be more aggressive for >$1M businesses (always
recommend hiring a CPA, always recommend dedicated bookkeeper) or more
permissive for <$50k (skip state filings until needed).

## Going further

- Pair with the [**Incorporation Agent**](../incorporation_agent/) —
  this agent assumes incorporation is done; if not, run that first.
- Pair with the [**Bank & Insurance Setup Agent**](../bank_insurance_agent/) —
  workers' comp registration is on both lists.
- Use the [**Business Plan Implementation Manager**](../../advanced_business_agents/multi_agent_apps/business_plan_implementation_manager/)
  for revenue projections — those drive nexus exposure planning.

## Footer

From **AI-Native Business Apps** — hand-built, provider-agnostic, Apache-2.0.
