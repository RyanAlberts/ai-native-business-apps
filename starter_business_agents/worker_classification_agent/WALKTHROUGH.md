# Walkthrough — Worker Classification Agent

## The scenario

You're a 5-person software startup in San Francisco. Your seed round is
running short. You want to hire a lead engineer at $150/hour, full-time,
in your office, on a laptop you'll provide. To avoid payroll setup and
the 7.65% employer-side FICA, you want to pay them as a 1099.

You ask the agent: "is this okay?"

## What happens, step by step

### Step 1 — call `classification_tests_reference`

Returns the canonical factor lists:
- IRS three categories: behavioral control, financial control,
  relationship of the parties (each with sub-factors).
- DOL 2024 economic-reality test: 6 factors (opportunity for profit/loss,
  investment, permanence, control, integral-to-business, skill/initiative).

The agent will name and apply these factors verbatim — no fabrication.

### Step 2 — call `state_classification_law_lookup`

You said California. Returns:

> California ABC test (AB5 / Labor Code §2775). Worker is presumed an
> employee unless ALL THREE of A, B, and C are satisfied:
>
>   A. Free from the hiring entity's control and direction;
>   B. Performs work outside the usual course of the hiring entity's business;
>   C. Customarily engaged in an independently established trade.
>
> FAIL ANY of A/B/C → W-2 employee.

The agent immediately applies A/B/C to your situation:

- **A. Free from control** — You set the schedule (9-5 in your office),
  provide the laptop. **FAILS A.**
- **B. Outside usual course of business** — You're a software company
  hiring a software engineer. The work IS your business. **FAILS B.**
- **C. Independent business** — Probably a fail too (worker doesn't
  have other clients).

Three fails. Verdict: **W-2 employee in California. NOT eligible for
1099 regardless of how the federal factors lean.**

The agent reports this without softening.

### Step 3 — federal analysis (for completeness)

Even though CA already forces W-2, the agent walks through the federal
tests:

**IRS three-category**:
- Behavioral control → **W-2** (set schedule, in-office, company laptop)
- Financial control → **W-2** (hourly pay, no investment by worker)
- Relationship → **W-2** (open-ended, integral to business, full-time)

**DOL six factors**:

| Factor | Lean | Why |
|---|---|---|
| Profit/loss | W-2 | Hourly pay — worker can't realize profit/loss |
| Investment | W-2 | Company provides laptop |
| Permanence | W-2 | Full-time, open-ended |
| Control | W-2 | 9-5, in-office, supervised |
| Integral to business | W-2 | Software dev at a software company |
| Skill/initiative | W-2 | No independent business; works only for you |

6 of 6 factors point W-2. Federal would also classify W-2.

### Step 4 — recommendation

- **Verdict**: W-2 employee.
- **Risk score**: HIGH if you do it as 1099 anyway (CA AB5 + federal both fail).
- **Set up payroll**: Gusto recommended for a 5-person startup (~$40/mo
  + $6/employee).
- **File**: W-2 + W-3 annually; Form 941 quarterly; Form 940 annually.
- **Contract type**: Employment Agreement — point at `legal_doc_agent`.

### Step 5 — quantify the cost of getting it wrong

If the founder ignores the recommendation and pays as 1099 anyway:

- Federal back payroll tax: 7.65% × $150/hr × 2080 hr/yr = ~$23,856
  per year per worker, with multi-year audit lookback.
- California civil penalty: $5,000–$25,000 per misclassified worker
  (Labor Code §226.8).
- Potential FLSA back-pay (overtime owed, since contractors don't get
  OT but employees do).
- Worker may sue for benefits (health, retirement) they didn't get.

### Step 6 — common mistakes section

- "We have an IC agreement so we're safe" — courts look at the
  relationship, not paperwork.
- "They want to be 1099" — the worker's preference doesn't determine
  classification.
- "We pay them through a 1099 platform like Deel" — Deel + similar are
  payroll PRODUCTS, not classification opinions. They'll happily run
  whatever you tell them.

## The agent's hard rules

1. Always call both tools (no fabricating factor names or state laws).
2. In ABC-test states, fail-any-prong overrides federal analysis. The
   agent does NOT soften this.
3. The agent does not generate the contract itself — that's
   `legal_doc_agent`. It recommends the right contract type and points
   there.
4. The agent never accepts "they want to be 1099" or "we have an IC
   agreement" as classification arguments.

## What the agent can't do

- Authoritatively determine if a worker qualifies for one of CA AB5's
  industry-specific exemptions (lawyers, accountants, certain creative
  professionals, real estate agents, etc.) — the exemption list is
  fact-intensive and updated periodically. The agent flags when an
  exemption might apply and recommends attorney review.
- Compute exact dollar penalties — the federal back-tax is computable
  given a wage and tenure; state penalties are discretionary and case-
  specific.
- Generate the employment / IC contract itself (use `legal_doc_agent`).

## Why this matters more than founders think

Misclassification is one of the most common and expensive payroll
mistakes in early-stage company building: a finding can mean back
payroll taxes, penalties, and multi-year retroactive assessments — and
signing an "Independent Contractor Agreement" does NOT settle the issue;
courts and agencies look at actual control, not the contract label.

(We deliberately don't quote a specific audit-rate or average-penalty
figure — those numbers vary widely by source and year and are easy to
get wrong. The point stands without a false-precision statistic.)

This is one of the most common, lowest-friction-to-make-correctly,
highest-cost-to-screw-up decisions in early-stage company building.
The agent makes the decision cheap.
