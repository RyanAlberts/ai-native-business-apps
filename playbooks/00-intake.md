# Playbook 00 — The Interview

**Who works:** the agent asks, the founder answers. No filings, no accounts, no documents today.
**Founder time:** 5–10 minutes.
**Gate:** `bash verify/journey_gate.sh 00` exits 0 — `company.json` exists with the required fields filled.

## Goal

Fill in the company profile **once** so no later phase re-asks for the same
facts. The answers become `company.json` — the same portable profile the
Python CLI uses, and the spine every specialist phase reads from.

Before the first question, say the disclaimer in one friendly line: Keel
prepares drafts and guidance, not legal or tax advice — a licensed
professional should review before anything gets filed.

## How to run the interview

Read the `Company` dataclass in `core/company.py` first — its fields are
the questions, and `company.json` must use exactly those field names. Ask
**one question at a time**, plain English, and skip anything the founder
already said in passing. If an answer is vague, reflect back a concrete
guess and let them correct it.

### The questions (mapped to `company.json` fields)

1. **The business, in one sentence** → `one_liner`. "What does the company
   do? Tell me like you'd tell a friend." Follow up until you can say it
   back in one plain sentence. Fold any liability worries they mention into
   `liability_notes` ("hardware lives in customer warehouses", "we handle
   health data", …).
2. **The name** → `legal_name`. "What's the company called?" A working name
   is fine — Phase 01 checks availability before anything is filed. A
   trade name / DBA, if different, goes in `dba`.
3. **Industry** → `industry`. One or two words.
4. **Home state** → `home_state`. "Which US state do you (the founders)
   live and work in?"
5. **State of formation** → `state_of_formation`. Only if they already have
   a preference ("Delaware", "same as home"). Blank = Phase 01 recommends.
6. **Entity preference** → `entity_type`. Only if they already have one
   (C-Corp / S-Corp / LLC). "Not sure" = blank; Phase 01 recommends.
7. **The founders** → `founders`. Name, role, and rough equity split for
   each (a list of `{name, role, equity_pct, email}` objects — email
   optional).
8. **Funding plans** → `funding_stage`. Bootstrap, SAFE / friends & family,
   priced seed in 9–18 months, or Series A+ track. This single answer does
   the most work in the entity recommendation — pin it down.
9. **Hiring plans** → `employees_plan`. Just founders, 1–5, or 6+ in the
   next 12 months.
10. **Stock issuance / formation date** → `formation_date` (ISO
    `YYYY-MM-DD`), if the company already exists or stock has already been
    issued. This is what makes the 83(b) deadline and the compliance
    calendar computable — if it's blank, say so: "once you have a real
    formation date, tell me and I'll recompute the deadlines." If the
    entity was formed on one date and stock was issued on another, record
    the issuance date in `notes` too — the 83(b) clock runs from
    *issuance*, and Phase 02 will use it.
11. **Anything else** → `notes`. Existing EIN (→ `ein`), pending trademark,
    licenses they know they need, and so on.

Do NOT ask for anyone's SSN, ITIN, or bank details — not now, not ever
(contract rule 5).

## Record and checkpoint

1. Write **`company.json`** at the repo root — valid JSON, exactly the
   `Company` field names, founders as a list of objects. Leave unknown
   fields as empty strings rather than omitting them.
2. Update **`PROGRESS.md`**: phase 00 done, date, one-line business
   summary in the Company summary section.
3. Read back a five-line summary: business, founders + split, home state,
   funding + hiring plans, and what happens next. Get an explicit "yes,
   that's right."

## Gate

`bash verify/journey_gate.sh 00` — checks `company.json` exists and
`legal_name`, `home_state`, and `one_liner` are non-empty (the same three
fields `Company.missing_for_formation()` requires). Then tell the founder
what Phase 01 does — "next I work out what kind of company to form and
where, and give you the exact filing checklist" — and continue or stop
cleanly.

## If things go wrong

- **Founder can't decide on a name:** use a working name, note
  `TENTATIVE` in `notes`, and move on — Phase 01's name-availability check
  is where it gets real.
- **Founder isn't US-based / wants a non-US entity:** say plainly that
  Keel's data and playbooks cover US formation (50 states + federal), and
  a cross-border setup needs a professional from the start. Don't improvise
  another country's process.
