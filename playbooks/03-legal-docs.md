# Playbook 03 — Founding Legal Documents

**Who works:** the agent drafts; the founder picks the document set and confirms key choices.
**Founder time:** ~10 minutes.
**Gate:** `bash verify/journey_gate.sh 03` exits 0.

## Goal

Draft the founding documents this company actually needs now — not a
template dump. Based on the Phase 01 entity decision and the founder count:
operating agreement (LLC) **or** bylaws (corporation), founder IP
assignment, an NDA template, and — for multi-founder companies — the
cofounder agreement with a real vesting schedule.

## The brief (your role for this phase)

Read `starter_business_agents/legal_doc_agent/prompts.py` and follow its
`SYSTEM_PROMPT` in full — the supported document types, the output sections
(Document type & scope → Key choices made → Document draft → clauses to
red-flag → state-specific considerations → mistakes → next steps →
disclaimer), and the cofounder-agreement special-handling block (equity
rationale, vesting, reverse vesting and its 83(b) interaction, IP
assignment, tie-breaking, departure mechanics). Frame the work with
`STEP_INSTRUCTIONS["legal_doc"]` from
`advanced_business_agents/multi_agent_apps/founding_journey/prompts.py` —
you are step 3; don't regenerate incorporation advice.

## Tool substitutions

| The brief says | You do |
|---|---|
| `cofounder_vesting_schedule(...)` | Compute the schedule yourself following the exact algorithm in `starter_business_agents/legal_doc_agent/tools.py`: monthly amount = total shares ÷ total months; cliff amount = round(monthly × cliff months); month-end-clamped dates; nothing vests before the cliff. Default to the industry standard the brief names (4 years, 1-year cliff, double-trigger) and surface the default. **Check your math before embedding it:** cumulative at the cliff equals the cliff amount, and the final month's cumulative equals the total share count. Show at least months 0 / cliff / 24 / 36 / 48. |

## Steps

1. Build the profile block from `company.json` + upstream decisions.
2. Propose the document set for THIS company in plain English and get the
   founder's yes (e.g. single-member Texas LLC → operating agreement + IP
   assignment + one-way NDA template; skip the cofounder agreement).
3. Draft each confirmed document per the brief — real drafts with
   `[BRACKETED]` placeholders only where a fact is genuinely unknown.
4. If any document embeds vesting or restricted shares, say the 83(b)
   consequence out loud and cross-reference the Phase 02 letter and
   deadline.
5. Write everything to **`formation-packet/03-legal_doc.md`** — one file,
   documents separated by `# ` headings, disclaimer footer at the end.
6. Update `PROGRESS.md`: phase 03 done, date, which documents were drafted
   and which key defaults the founder should revisit with an attorney.

## Gate

`bash verify/journey_gate.sh 03` — checks the artifact exists, contains at
least one signature block, and carries the footer.

## If things go wrong

- **Founder asks for a document the brief declines** (court filing,
  immigration form): decline as the brief says, recommend a licensed
  attorney, and note it in `PROGRESS.md` — the phase still completes with
  the documents that ARE in scope.
- **Founders haven't settled their equity split:** don't freeze the
  journey. Draft with the split marked `[TO BE AGREED]`, put the
  cofounder-agreement risks section front and center, and flag in
  `PROGRESS.md` that the split is the single most important open item.
