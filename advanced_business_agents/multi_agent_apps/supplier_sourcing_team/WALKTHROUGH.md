# Walkthrough — Supplier Sourcing Team

> "I'm launching a DTC kitchenware brand. I need to find a manufacturer
> who can make 5,000 units of silicone product to FDA food-safe standards
> for under $4 a unit. I have no idea where to start."

Most founders Google "alibaba supplier" and walk into a maze. This agent
provides the actual sourcing workflow procurement teams use at bigger
companies, scaled down for a solo founder.

## What you'll see

Run `agent supplier-sourcing` and fill in the sourcing form. Over 4 stages
you get:

1. **Sourcing** — A category map (contract manufacturer vs. distributor
   vs. fabricator), geographic recommendation (likely "Asia primary, MX
   nearshore as a hedge" for kitchenware at this volume + price), a long
   list of 8–12 named candidates with MOQs, lead times, what they're
   known for. If WebSearch is enabled, these are real companies; if not,
   they're clearly-labeled *types* + directory pointers.

2. **Vetting** — A scoring rubric: 8–10 criteria with weights, evidence
   to look for, disqualifying red flags (refusing NDA, opaque pricing,
   non-standard payment, etc.), 15–25 qualifying questions to send to
   each supplier, a sample collection plan, audit recommendations.

3. **RFP Draft** — A ready-to-send Request for Proposal: requirements
   section, info requested from suppliers, evaluation criteria (showing
   the supplier how you'll score them — they respond better when they
   know), submission instructions, terms. Plus a cover-email template
   the founder pastes when sending.

4. **Comparison Matrix** — A markdown table (rows = criteria, columns =
   `[Supplier A]` through `[Supplier E]`) the founder fills in as RFP
   responses come in. Plus a scoring rubric defining what 1/3/5 looks
   like on each criterion, a weighted-total worksheet with an example
   calculation, a negotiation playbook for the top 2, pilot-order
   strategy, and walk-away triggers during the pilot.

## How it works

`core.SequentialHarness` with 4 stages. Stage 1's named-supplier
suggestions rely on `WebSearch` (Claude built-in, on by default in
config). If you switch providers, sourcing degrades but the rest of the
pipeline is unaffected.

## Customizing it

### Add a logistics stage

Append a 5th `Stage` to `agent.py::_stages()` for freight forwarding +
customs broker selection. The harness handles N stages.

### Tighten the vetting rubric

Edit `VETTING_PROMPT`'s criteria table. Common founder tweaks:
- Add an ESG / sustainability row
- Add a working-capital row (their payment terms)
- Add an exclusivity row (will they not sell same product to competitors?)

### Disable WebSearch for cost / portability

```yaml
allowed_tools: []
```

Stage 1 still produces useful output (categories + directories like
Alibaba, Thomasnet, Maker's Row, IndustryNet) but won't name actual
companies.

## Going further

- Pair with the [**Legal Doc Generator**](../../../starter_business_agents/legal_doc_agent/)
  for the NDA you'll send with the RFP, and the Service Agreement / SOW
  for the eventual contract.
- Pair with the [**Business Plan Implementation Manager**](../business_plan_implementation_manager/)
  to validate that the unit-economics for your target market work before
  committing to a supplier minimum order quantity.

## Footer

From **AI-Native Business Apps** — hand-built, provider-agnostic, Apache-2.0.
