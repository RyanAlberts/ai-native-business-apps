# Delaware Franchise Tax Calculator

**What Carta / LegalZoom charge**: Carta charges to recompute (mid-tier
plans only); LegalZoom files the annual report ($199+) but doesn't
recompute. Boutique startup CPAs charge $200–500 to fix the bill.
**What this agent charges**: $0. Pure math.

## The pain

Delaware's billing system defaults C-Corps to the **Authorized Shares
method**. For a typical early-stage startup (10M authorized shares,
8M issued, par $0.0001, ~$50K of year-end assets), the default bill is:

> **$85,165** under Authorized Shares

The same company, on the same filing, can elect the **Assumed Par Value
Capital method**:

> **$400** under APVC

That's a real $84,765 founders panic-pay because they don't know they
can recompute. It happens every March 1.

## What it does

Computes both methods, surfaces the recommendation, walks through the
APVC math step-by-step using your actual numbers, and points you at the
DE payment portal with instructions to select the APVC radio button.

Two deterministic tools:

- `delaware_franchise_tax_calc(authorized, issued, par, gross_assets)`
  — both methods + APVC breakdown + total due (includes $50 annual
  report fee) + recommendation + savings.
- `delaware_llc_flat_tax(entity_type)` — DE LLCs/LPs/GPs pay flat $300/yr
  (no franchise math); this returns the facts and the due date (June 1).

Pure-Python. No network. No LLM math.

## Quick start

```bash
# CLI
python -m starter_business_agents.delaware_franchise_tax_agent.agent \
  "10M authorized, 8M issued, par $0.0001, year-end assets ~$50K. DE wants $85K."

# Streamlit UI (form inputs)
streamlit run starter_business_agents/delaware_franchise_tax_agent/app.py
```

## Inputs you need

| Input | Where to find it |
|---|---|
| Authorized shares | Certificate of incorporation |
| Issued / outstanding shares | Cap table as of December 31 of the tax year |
| Par value per share | Certificate of incorporation (commonly $0.0001) |
| Total gross assets | Federal Form 1120 Schedule L, line 15, end-of-year column |

## NOT legal or tax advice

This is procedural guidance based on Delaware's published formulas
(8 Del. C. §§ 501–507). The math is mechanical, but verify your
gross-assets number with a CPA before submitting — it's the only input
that depends on your books and getting it wrong shifts everything.

## Filing deadline

**March 1** each year for the prior calendar year (C-Corps).
**June 1** for LLCs / LPs / GPs.

Late penalty: $200 + 1.5% monthly interest, plus loss of good standing.

## Sources

- DE Franchise Tax Calculator (official): https://corp.delaware.gov/frtaxcalc/
- DE Pay Franchise Tax: https://corp.delaware.gov/paytaxes/
- Statute: 8 Del. C. §§ 501–507
