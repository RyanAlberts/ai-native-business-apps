# Walkthrough — Delaware Franchise Tax Calculator

## The scenario

It's late February. Your Delaware C-Corp got an email from the DE
Division of Corporations. The email says you owe **$85,165** in franchise
tax + a $50 annual report fee. Due March 1.

You've been operating for a year. Revenue is ~$30K. You have one
employee. Total assets on the balance sheet are about $50K (mostly the
remaining seed cash). The $85,165 bill is more than 2× your annual
revenue and would zero your bank account.

## Why the bill is that high

Delaware computes C-Corp franchise tax under one of two methods. Their
billing system defaults to the **Authorized Shares method** — and
because you (or your formation lawyer, or your founder template)
authorized **10,000,000 shares** at incorporation (standard for
VC-track startups), the default formula:

```
$250 base (5,001–10,000 shares)
+ $85 per additional 10,000 shares (or portion thereof)
```

…produces a tax of about $85,000.

That formula is correct. It's also not the method you have to use.

## The other method

Delaware code 8 Del. C. § 503(3) lets you elect the **Assumed Par Value
Capital (APVC) method** instead. The APVC formula:

```
1. assumed_par = total_gross_assets / issued_shares
2. effective_par = max(assumed_par, par_value_per_share)
3. APVC = effective_par × authorized_shares
4. round APVC up to the next $1,000,000
5. tax = $400 per million
6. floor at $400, cap at $200,000
```

For your situation:

| Step | Value |
|---|---|
| Total gross assets | $50,000 |
| Issued shares | 8,000,000 |
| `assumed_par` | $50,000 / 8,000,000 = **$0.00625** |
| `par_value_per_share` | $0.0001 |
| `effective_par` (max) | **$0.00625** |
| Authorized shares | 10,000,000 |
| APVC | $0.00625 × 10,000,000 = **$62,500** |
| Rounded up to next million | **1** |
| Tax = 1 × $400 | **$400** |
| Plus annual report fee | + $50 |
| **Total due** | **$450** |

You save **$84,765**.

## What the agent produces

A markdown report with:

1. **TL;DR** — "Pay $450 under APVC, not $85,215 under Authorized Shares.
   Savings: $84,765."
2. **Side-by-side table** of both methods.
3. **Plain-English explanation** of why the default bill is so high.
4. **The APVC calculation walked through step by step** using your actual
   numbers (from the tool's `assumed_par_value_breakdown` output).
5. **How to file**: open the DE portal, log in with your File Number,
   *select the Assumed Par Value Capital radio button*, enter your
   inputs, pay $450.
6. **Common mistakes** (paying the default; using year-START assets
   instead of year-END; missing March 1 entirely).
7. **Disclaimer** — verify gross-assets with a CPA, this is procedural
   guidance not tax advice.

## What it doesn't do

- File for you (DE portal requires manual login + payment).
- Verify your gross-assets number against your books.
- Handle the unusual case where you authorized 1 billion+ shares (the
  cap kicks in at $200K either way; you may have a structural problem).

## When APVC LOSES

For a true tiny entity (≤5,000 authorized shares, no issued shares yet),
the Authorized Shares method ($175) beats the APVC floor ($400). The
agent flags this and recommends the cheaper option — same logic, just
inverted.

## Edge cases the tool handles

| Input | Result |
|---|---|
| `issued_shares=0` (newly formed) | APVC method returns $400 floor + a note |
| `authorized_shares=0` | Error: must be > 0 |
| Negative values | Error: must be non-negative |
| `gross_assets=0` | APVC returns $400 floor (the assumed-par numerator is 0) |
| 200M+ authorized shares | Either method capped at $200K |

## Sources

- Delaware Division of Corporations Franchise Tax Calculator:
  https://corp.delaware.gov/frtaxcalc/
- Pay Franchise Tax portal:
  https://corp.delaware.gov/paytaxes/
- Statute: 8 Del. C. §§ 501–507
