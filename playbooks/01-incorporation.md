# Playbook 01 — Incorporation

**Who works:** the agent, with one decision from the founder (entity + state).
**Founder time:** ~10 minutes.
**Gate:** `bash verify/journey_gate.sh 01` exits 0.

## Goal

Choose the entity type and state of formation, and produce the exact filing
plan — checklist with real portal links, registered-agent options, and
costs. Later phases depend on this decision, so it's made first and made
explicitly.

## The brief (your role for this phase)

Read `starter_business_agents/incorporation_agent/prompts.py` and follow
its `SYSTEM_PROMPT` in full — the output sections (Disclaimer →
Recommendation summary → Entity type → State of formation → Filing
checklist → Key documents → Registered agent options → Estimated costs →
Common pitfalls) and all of its rules. Frame the work with
`STEP_INSTRUCTIONS["incorporation"]` from
`advanced_business_agents/multi_agent_apps/founding_journey/prompts.py` —
you are step 1 of 5, so state the chosen entity and state explicitly near
the top.

## Tool substitutions (you have no Python tools — read the files instead)

| The brief says | You do |
|---|---|
| `state_portal_lookup(state)` | Open `core/state_portals.py`, find `STATE_PORTALS["<code>"]` for the recommended state (and `FEDERAL_PORTALS` below it). Use those URLs, fees, and notes **verbatim**. If the founder asks about a second state, look that one up too and contrast costs. |
| `state_business_name_search(state, name)` | Same file: the state's `business_name_search_url`. Follow the search method described in `starter_business_agents/incorporation_agent/tools.py` (exact name, then root words, then confusingly-similar variants) and put the URL + method in the Filing Checklist for the founder to run in their browser. |

Never substitute a URL or fee from memory — if a state's entry is missing
or thin, say so and link the state's main Secretary of State page from the
same file.

## Steps

1. Build the `## Known company profile` block from `company.json` (contract
   → "How to work a playbook").
2. Produce the full analysis per the brief. Recommend decisively — one
   entity type, one state — with the reasoning tied to THIS founder's
   funding, hiring, and liability answers.
3. **Get the founder's yes** on entity type + state of formation (contract
   rule 8). Present the recommendation in three or four plain sentences,
   then ask. If they override, honor it and note their reasoning.
4. Write the confirmed decision into `company.json`: `entity_type`,
   `state_of_formation` (and `dba` if one came up).
5. Write the full markdown output to **`formation-packet/01-incorporation.md`**
   (create the folder if needed), ending with the disclaimer footer.
6. Update `PROGRESS.md`: phase 01 done, date, the decision in one line
   ("Delaware C-Corp — priced seed planned within 12 months").

## Gate

`bash verify/journey_gate.sh 01` — checks the artifact exists with its core
sections and footer, and that `company.json` now carries a non-empty
`entity_type` and `state_of_formation`.

## If things go wrong

- **The company already exists** (`formation_date` is set / stock was
  issued): don't recommend filing a new entity. Confirm the existing
  entity type and state with the founder, record them in `company.json`,
  and reframe the filing checklist as verify-and-complete — is the EIN in
  hand, the registered agent designated, anything from the checklist still
  missing? The rest of the journey proceeds normally.
- **The name search finds a conflict:** don't stall the journey on
  naming. Help the founder pick a distinguishable variant or mark the name
  `TENTATIVE` in `notes` and continue — but say clearly that nothing gets
  filed until the name clears the state's own search.
- **Founder wants an entity/state combination the brief argues against**
  (e.g. Delaware for a bootstrapped single-founder consultancy): state the
  trade-off once, plainly, then follow their call (and record in
  `PROGRESS.md` that it was their call).
