# 🏭 Supplier Sourcing Team

> Sequential 4-stage pipeline — Sourcing → Vetting → RFP → Compare —
> that takes you from "I need this made" to a ready-to-send RFP and a
> scoring rubric for picking the winner.

## Pipeline

| # | Stage | Output |
|---|---|---|
| 1 | **Sourcing** | Category map, geographic strategy, long list of 8–12 candidate suppliers, channels to find more. |
| 2 | **Vetting** | Vetting criteria table (weights, evidence, red flags), 15–25 qualifying questions, sample/audit plan, short-list rubric. |
| 3 | **RFP Draft** | Ready-to-send RFP: requirements, info requested, evaluation criteria, submission instructions, cover email template. |
| 4 | **Comparison** | Matrix template, scoring rubric (1/3/5 definitions per criterion), weighted total worksheet, negotiation playbook, pilot strategy, walk-away triggers. |

Stage 1 uses `WebSearch` by default (Claude built-in) to sniff for real
suppliers in the category. Without it, the agent produces a clearly-labeled
list of supplier *types* + directories where to find named candidates.

## Run

```bash
agent supplier-sourcing
agent supplier-sourcing --cli "Contract-manufactured silicone kitchenware, 5k units initial, $4/unit, FDA food-safe, open to US/MX/Asia."
```

Pipeline runtime: ~8–10 minutes end-to-end on `claude-sonnet-4-6`
with `WebSearch` (per-stage ~120–140s × 4 stages, verified
2026-05-14 — Comparison stage in particular is heavy on synthesis and
runs longer than the earlier stages). Set client timeouts ≥ 600s when
scripting against this agent.

## Use cases

- DTC brand sourcing manufactured goods (apparel, kitchen, beauty, etc.)
- SaaS founder sourcing a development or design agency
- Restaurant operator finding food / beverage / equipment vendors
- B2B service business finding white-label suppliers

## Customize

- **Disable WebSearch** if running on non-Claude providers — set
  `allowed_tools: []` in `config.yaml`. Stage 1 will produce category +
  directories instead of named suppliers.
- **Add a stage** (e.g. "Logistics Plan" for freight forwarding + customs)
  by appending to `_stages()` and `prompts.py`.
- **Adjust the vetting weights** by editing the table in
  `VETTING_PROMPT`.

## Provider parity

Verified on Claude with WebSearch. Without web access, sourcing quality
degrades to "categories + directories" rather than named suppliers — still
useful, less complete. See [PARITY.md](./PARITY.md).
