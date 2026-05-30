# Walkthrough — 83(b) Election Agent

A narrative tour of what the agent actually does end-to-end, and why each
piece exists.

## The problem

You just received restricted stock — most likely founder shares with a
4-year vesting schedule and a 1-year cliff. The IRS taxes you on the
spread between FMV and the price you paid, but **when** the tax bill
hits depends on whether you file an §83(b) election:

| Filed §83(b) within 30 days? | What you owe in year 0 | What you owe over the next 4 years |
|---|---|---|
| Yes | Tax on the (usually tiny) spread *today* | $0 on vesting; capital gains only on sale |
| No | $0 today | Ordinary income tax on the spread between FMV and price-paid at **each** vesting date for 4 years |

For a founder who buys stock at par ($0.0001/share) when FMV is also
par, "today's spread" is essentially $0 — so the 83(b) costs nothing now
and saves potentially six figures later. But it's irrevocable, and the
30-day deadline is a statutory bright line.

## Why most founders miss it

- They don't know the rule.
- They incorporated outside Stripe Atlas (which auto-files for its
  customers), so no one prompts them.
- They couldn't find a clear, current template — the IRS's own model
  election text is buried in a 2012 revenue procedure.
- They didn't know which IRS service center to mail it to.
- They mailed it without certified return-receipt and have no proof.

## What this agent does

You give it (in free text or via the Streamlit form):

- Your name, address, state of residence
- The company (issuer) name, state, EIN
- The grant date
- Share count, class, FMV per share, price paid per share
- Vesting / repurchase restrictions

The agent then:

### Step 1 — call `eighty_three_b_deadline_check`

Pure date math. Returns:
- Postmark-by date: grant_date + 30 days
- Days remaining: postmark_by - today
- Urgency: `URGENT` (≤3 days) / `NEAR` (≤10) / `OK` (>10) / `EXPIRED`

The agent surfaces this **at the top of the output**, in bold, before
anything else. If urgency is `EXPIRED`, the agent stops generating a
routine letter and instead recommends consulting a tax attorney about
§9100 discretionary relief.

### Step 2 — call `irs_service_center_for_state`

Table lookup. Returns the correct IRS service-center address (`Kansas
City, MO 64999-0002` for most states; `Ogden, UT 84201-0002` for most
western states). Also returns the IRS lookup URL — the agent ALWAYS
tells the founder to verify the address on irs.gov before mailing,
because the IRS reroutes service centers periodically.

### Step 3 — assemble the election letter

Following the model text from IRS Rev. Proc. 2012-29:

```
ELECTION TO INCLUDE IN GROSS INCOME IN YEAR OF TRANSFER OF PROPERTY
PURSUANT TO SECTION 83(b) OF THE INTERNAL REVENUE CODE
...
```

Every field that requires a personally-identifying number (SSN, ITIN)
is left as a `[TIN]` placeholder — the agent does NOT echo SSNs back
in plain text even if the founder provides one. The founder hand-fills
the TIN on the printed letter before signing.

### Step 4 — mailing instructions

Numbered, opinionated:
1. Print two copies, sign the original.
2. USPS Certified Mail with Return Receipt (Green Card).
3. Verify the IRS address on irs.gov first.
4. Mail a copy to the issuer too (the regulation requires it).
5. Optional: file electronically via IRS Form 15620 (newer option).

### Step 5 — calendar reminder (.ics)

The agent emits a complete `.ics` block the founder can save as a file
and import. The event is on the postmark-by date with the IRS address
embedded in the description.

### Step 6 — tax-savings illustration

Using the founder's own FMV and price-paid numbers, the agent walks
through what gets recognized as income at filing vs. what would be
recognized later without the election. If FMV equals price-paid (most
common at founding), the agent flags that the win is maximal: $0 now,
capital gains later on sale.

### Step 7 — post-filing checklist

- Keep the certified-mail receipt forever (it's your audit defense).
- Keep a copy of the letter with your permanent tax records. (You no
  longer attach it to your Form 1040 — TD 9779 removed that requirement
  in 2016.)
- Update your cap-table tool to record that an 83(b) was filed.
- Tell your CPA.

## What it deliberately doesn't do

- **Sign or mail anything for you.** The election is irrevocable and
  requires your wet signature. The agent gives you the letter, not a
  filed letter.
- **Echo your SSN.** The agent will accept it as input (to validate
  you're a US taxpayer) but won't render it in the output.
- **Generate PDFs.** Markdown out, founder formats as needed. Future
  enhancement.
- **Tell you whether you should file.** That's a tax question for your
  CPA. The agent assumes you've already decided to file.

## Failure modes the prompt guards against

- Made-up dates: the prompt requires calling `eighty_three_b_deadline_check`
  first and instructs the model never to invent dates.
- Made-up IRS addresses: same pattern with `irs_service_center_for_state`.
- "You can file late" reassurance: the prompt explicitly forbids this —
  the 30-day window is statutory, §9100 relief is rare and discretionary.
- Stale data: every IRS address response surfaces the lookup URL so the
  founder verifies.
