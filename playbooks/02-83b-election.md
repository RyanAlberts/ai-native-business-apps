# Playbook 02 — The 83(b) Election

**Who works:** the agent drafts; the founder supplies the letter details.
**Founder time:** ~10 minutes (more only if they need to dig up share numbers).
**Gate:** `bash verify/journey_gate.sh 02` exits 0.

## Goal

Determine whether an 83(b) election applies to this company, and if it
does, produce the ready-to-print letter, the postmark deadline, the correct
IRS mailing address, and the calendar reminder. The 30-day window is
statutory and unforgiving — this phase runs early for exactly that reason.

## The brief (your role for this phase)

Read `starter_business_agents/election_83b_agent/prompts.py` and follow its
`SYSTEM_PROMPT` in full — the deadline-first output format, the required
letter fields, the Rev. Proc. 2012-29 letter structure, mailing
instructions, the `.ics` reminder block, and every rule (especially: mask
TINs, never call a late filing harmless, no routine letter if the window is
EXPIRED). Frame the work with `STEP_INSTRUCTIONS["election_83b"]` from
`advanced_business_agents/multi_agent_apps/founding_journey/prompts.py` —
use the entity decision from Phase 01; if it's an LLC taxed as a
partnership or a sole proprietorship, say clearly whether an 83(b) applies
instead of forcing a letter.

## Tool substitutions

| The brief says | You do |
|---|---|
| `eighty_three_b_deadline_check(grant_date)` | Do the arithmetic yourself and show it: get today with `date +%F`, postmark deadline = grant date + 30 **calendar** days. Urgency bands per the logic in `starter_business_agents/election_83b_agent/tools.py`: past = **EXPIRED**, ≤3 days left = **URGENT**, ≤10 = **NEAR**, else **OK**. Use that file's IRS e-file (Form 15620) and Rev. Proc. URLs verbatim. |
| `irs_service_center_for_state(state)` | Read the `_STATE_TO_CENTER` table in the same `tools.py` for the founder's state of residence. Always include the IRS "where to file" lookup URL from that file and the reminder that addresses change — verify before mailing. |

The grant date is `formation_date` from `company.json` unless the founder
gives an actual stock-issuance date (check `notes` — Phase 00 records it
there when the two differ) — ask which applies. If there's no date yet
(stock not issued), there is no deadline to compute: explain that the
30-day clock starts at issuance, put a prominent "file within 30 days of
issuance" action in the output, and move on. Date-arithmetic flags differ
by platform (`date -d` vs `date -j -v+30d`) — any method is fine as long
as you show the resulting date and sanity-check it by hand.

**One election per person, not per company.** Every founder whose stock is
subject to vesting files their own 83(b) — draft a separate letter (with
its own share numbers and mailing address) for each of them, and say
plainly that each founder mails theirs individually.

## Steps

1. Build the profile block from `company.json` + the Phase 01 decision.
2. Eligibility first (per the brief): restricted stock subject to vesting?
   Right entity type? Inside the window?
3. Collect the letter fields the brief lists (name, mailing address, share
   count/class, FMV and price paid, vesting terms). **Never ask for the
   SSN/ITIN** — the letter keeps `[TIN]` placeholders the founder fills in
   after printing. Anything the founder doesn't have handy stays a
   `[BRACKETED]` placeholder.
4. Produce the full output per the brief — deadline banner, letter,
   mailing instructions, `.ics` reminder block, tax-savings illustration
   (their numbers only), post-filing checklist.
5. Write it to **`formation-packet/02-election_83b.md`**, disclaimer footer
   at the end.
6. Update `PROGRESS.md`: phase 02 done, date, and the postmark deadline (or
   "no stock issued yet — clock not started") in the notes.

## Gate

`bash verify/journey_gate.sh 02` — checks the artifact exists, addresses
the postmark deadline, and carries the footer.

## If things go wrong

- **The window is EXPIRED:** follow the brief — no routine letter; the
  output explains the situation and says to contact a tax attorney about
  §9100 relief. That still completes this phase (the packet must reflect
  reality, not wishful dates).
- **Founder is a non-US taxpayer / ITIN case:** flag the extra complexity
  per the brief, recommend specialized advice, and keep placeholders in the
  letter rather than guessing.
