# Playbook 05 — Compliance & Tax Calendar

**Who works:** the agent, entirely. The founder confirms which states they operate in.
**Founder time:** ~5 minutes.
**Gate:** `bash verify/journey_gate.sh 05` exits 0.

## Goal

Map the recurring obligations — sales-tax nexus, state registrations,
federal and state annual filings, bookkeeping — and turn every dated
deadline into a calendar the founder can import. This is the phase that
keeps the company alive after Day 0.

## The brief (your role for this phase)

Read `starter_business_agents/compliance_tax_agent/prompts.py` and follow
its `SYSTEM_PROMPT` in full — nexus analysis, state registrations, federal
and state filing lists, bookkeeping setup, advisors, pitfalls, the
30/60/90-day plan, and the embedded compliance calendar. Honor its honesty
rules: thresholds as ranges with "verify", no filings the founder doesn't
need, and its BOI framing exactly as written. Frame the work with
`STEP_INSTRUCTIONS["compliance_tax"]` from
`advanced_business_agents/multi_agent_apps/founding_journey/prompts.py` —
you are step 5; be explicit about dates and cadences so they can go on a
calendar.

## Tool substitutions

| The brief says | You do |
|---|---|
| `state_compliance_lookup(states)` | Open `core/state_portals.py` and pull each operating state's entry (`annual_report_url`, `annual_fee_approximate`, `sos_business_filings_url`, `notes`) plus `FEDERAL_PORTALS`. Use them **verbatim**. States list = state of formation + every state of operation — confirm that list with the founder before you start. |
| `generate_compliance_ics(events)` | Build the `.ics` yourself following the emitter in `starter_business_agents/compliance_tax_agent/tools.py`: all-day `VEVENT`s (`DTSTART;VALUE=DATE` / next-day `DTEND`), a 7-day-out `VALARM` on each, ISO dates only. For each deadline use the FIRST upcoming occurrence (get today with `date +%F`). Embed the calendar in a fenced code block in the "Compliance calendar (.ics)" section with the same save-and-import instructions the tool returns (copy-paste from rendered markdown can lose the CRLF line endings the spec wants, so also tell the founder the deterministic `compliance-deadlines.ics` file from Phase 06 is the strict-importer fallback). Only include events whose dates you can state from facts — a deadline you'd have to guess stays in the narrative table marked "verify", not in the calendar. |

## Steps

1. Build the profile block from `company.json` + upstream decisions, and
   confirm the operating-states list with the founder (one question).
2. Produce the full analysis per the brief.
3. Assemble every dated deadline you named and generate the embedded
   `.ics` per the substitution above.
4. Write it to **`formation-packet/05-compliance_tax.md`**, disclaimer
   footer at the end.
5. Update `PROGRESS.md`: phase 05 done, date, the 2–3 highest-priority
   compliance items in one line.

## Gate

`bash verify/journey_gate.sh 05` — checks the artifact exists, includes the
annual-obligations analysis and an embedded calendar block, and carries the
footer.

## If things go wrong

- **Many operating states** (remote team, e-commerce everywhere): don't
  produce a 50-state wall. Cover formation + physical-presence states
  fully, explain the economic-nexus *trigger* once, and recommend a sales
  tax tool or CPA at the volume where per-state tracking stops being a
  founder job.
- **A state's entry in `core/state_portals.py` is thin or marked
  uncertain:** link the state's main SoS page from the same entry and say
  "verify on the state site" — never fill the gap from memory (contract
  rule 2).
- **The company sells SaaS or digital products:** don't apply the brief's
  "services usually aren't taxed" relief as a blanket rule — whether SaaS
  counts as a taxable service varies by state. Name it as a specific
  question for the CPA (or the state DOR pages you've already linked)
  rather than asserting per-state answers the repo's data doesn't carry.
