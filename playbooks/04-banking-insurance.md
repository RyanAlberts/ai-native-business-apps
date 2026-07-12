# Playbook 04 — Banking & Insurance

**Who works:** the agent, entirely. The founder just reads the plan.
**Founder time:** ~5 minutes.
**Gate:** `bash verify/journey_gate.sh 04` exits 0.

## Goal

A concrete banking + insurance plan: which business bank account to open
(and the documents to bring), and which insurance policies this business
actually needs — ranked, with realistic cost ranges. Plan only: the founder
opens the account and buys the policies themselves (contract rule 4).

## The brief (your role for this phase)

Read `starter_business_agents/bank_insurance_agent/prompts.py` and follow
its `SYSTEM_PROMPT` in full — the two-part structure (banking, then
insurance), the comparison tables, the documents-to-gather checklist, the
pitfalls, and the 30-day action plan. Mind its warning about the two
different "beneficial ownership" things — the bank's own form is a banking
step; don't turn it into a federal filing scare. Frame the work with
`STEP_INSTRUCTIONS["bank_insurance"]` from
`advanced_business_agents/multi_agent_apps/founding_journey/prompts.py` —
you are step 4, and the EIN is a prerequisite for opening the account, so
sequence it after the EIN step from Phase 01's checklist.

## Tool substitutions

None — this specialist has no deterministic tools. Institution and carrier
names come from the brief's own lists; costs are ranges marked
"approximate", exactly as the brief requires. Don't invent fee numbers.

## Steps

1. Build the profile block from `company.json` + upstream decisions (the
   entity type changes what the bank asks for; the industry and
   `liability_notes` drive the insurance ranking).
2. Produce the full plan per the brief, specific to this founder — a
   bootstrapped solo consultancy does not get a D&O pitch.
3. Write it to **`formation-packet/04-bank_insurance.md`**, disclaimer
   footer at the end.
4. Update `PROGRESS.md`: phase 04 done, date, the top bank pick and the
   2–3 policies recommended, in one line.

## Gate

`bash verify/journey_gate.sh 04` — checks the artifact exists, covers both
banking and insurance, and carries the footer.

## If things go wrong

- **Founder wants you to open the account or request quotes for them:**
  that's theirs to do (contract rule 4). Give them the documents checklist
  and the exact next click instead.
- **Regulated or unusual industry** (cannabis, firearms, crypto, money
  services): flag that many banks refuse these categories, name the issue
  plainly, and recommend they confirm the bank's policy before applying —
  don't present the standard picks as guaranteed to work.
