# Walkthrough — Business License + DBA Agent

## The problem

US business licensing is fragmented across four layers (federal, state,
county, city) and ~19,000 municipalities. Founders routinely either:

1. Pay a "business license service" $99–$300 for a checklist that's
   often partial or out of date.
2. Operate without one of the layers (typically city or county) and
   either get cited or — worse — find their entity's liability shield
   challenged in a dispute because they were operating without
   authorization.

Per the founder pain-point research:

> "The 'DBA vs. business license vs. home occupation permit' trio is
> wildly state-specific. Texas has no state business license but counties
> do; California has no state license but most counties require one;
> Massachusetts files DBAs at the city/town clerk level, not state.
> Even sophisticated founders confuse the three, and online formation
> services do not handle local permits at all."

## How the agent handles it

The agent is a **hybrid**:

- The deterministic taxonomy lives in `tools.py`. 51 US jurisdictions
  × DBA filing level (state / county / city / state+county / not_required).
  5 states with general state licenses (AK, DE, HI, NV, WA).
- The long-tail (city + county license URLs, industry-specific permits)
  comes from WebSearch at runtime.

This split is deliberate: the taxonomy is stable enough to hand-curate
(and faster than a search), while the long-tail is too sprawling to
hand-curate (and changes too often).

## A walked example

Founder input:

> "California LLC operating a specialty coffee shop. 1234 Mission St,
> San Francisco, CA 94110 (San Francisco County). On-premise kitchen
> baking pastries, indoor + sidewalk seating, beer/wine license planned.
> 2 employees year 1. LLC is 'Mission Coffee LLC' DBA 'The Daily
> Grind'."

### Step 1 — `dba_filing_jurisdiction("CA")`

Returns: `level: "county"`. CA files DBAs at the county clerk. San
Francisco County maintains its own FBN system.

### Step 2 — `state_general_business_license("CA")`

Returns: `general_state_license_required: false`. CA does NOT have a
general state business license. Founders waste hours looking for one;
the agent saves them by saying so explicitly.

### Step 3 — WebSearch for industry-specific state licenses

Coffee + food + beer/wine triggers:

- CA Dept of Public Health → **Retail Food Permit** (state level)
- CA Dept of Tax & Fee Administration → **Seller's Permit** (sales tax)
- CA Dept of Alcoholic Beverage Control → **Type 41 license** (beer +
  wine, bona fide eating place)
- CA Employment Development Department → employer registration (UI,
  ETT, SDI withholding)

### Step 4 — WebSearch for San Francisco County

San Francisco County uses the **SF Office of the Assessor-Recorder**
for FBN filings + the **SF Treasurer & Tax Collector** for the Business
Account / Business Registration. Found the URLs.

### Step 5 — WebSearch for City of San Francisco

San Francisco's **Business Registration Certificate** ($98 to $40,000
based on gross receipts, billed annually) + **Health Permit** from SF
Dept of Public Health (food service tier) + **Place of Entertainment
Permit** if amplified music + **Sidewalk Seating Permit** through SF
Public Works.

### Step 6 — synthesize

The agent emits the structured checklist with all of the above, in the
correct filing sequence (entity formed → EIN → DBA → state food permit
→ ABC liquor license → SF Business Registration → SF Health Permit →
sidewalk seating permit), plus an approximate year-1 total (~$1,500–
$4,500 in licenses + permits, ABC the largest single line).

## What the agent doesn't do

- **File for you**: every license requires its own application portal
  + payment. The agent points you at each.
- **Track changes**: when SF changes its Business Registration fee
  schedule (which happens annually), the agent's WebSearch result will
  catch the change but the snapshot is by definition stale by next year.
- **Replace zoning verification**: home-occupation permits depend on
  the property's zoning AND the building's CC&Rs / HOA rules / lease
  terms — the agent flags zoning as a separate check.

## When to consult an actual attorney

- Industries with safety- or money-handling-specific rules (medical,
  financial advisor, transportation, cannabis, alcohol distribution).
- Multi-state operations where each state's licensing layers stack.
- Federal-layer industries (ATF, FAA, FCC, SEC, FDA, DOT, MSHA).
- Any time city or county staff give conflicting answers (genuinely
  common in older cities with overlapping ordinances).

The agent's job is to give the founder a complete, current starting
point — not to replace the boutique attorney consult when the
licensing layer is unusually complex.

## Pattern extension

If the founder asks for the SAME analysis for a second location in a
different city, the agent runs the WebSearch portion afresh for the
new city + county, and the deterministic state-level data is unchanged
(unless the new location is in a different state).

If the founder's industry triggers FEDERAL licensing (e.g. selling
alcohol → ATF Federal Basic Permit; selling firearms → ATF Federal
Firearms License), the agent surfaces that explicitly and points at
the federal application portal.
