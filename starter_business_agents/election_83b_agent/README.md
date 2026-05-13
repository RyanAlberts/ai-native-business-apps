# 83(b) Election Agent

**What LegalZoom charges**: nothing — they don't sell §83(b) at all.
**What Stripe Atlas charges**: bundled into their $500 formation product
(Auto-83(b)) and only available to their formation customers.
**What this agent charges**: $0. Open source. Free under a Claude Max
subscription or any provider you bring keys for.

## What it does

Prepares the IRS §83(b) election letter — the time-sensitive filing
every founder with restricted-stock vesting must postmark within **30
calendar days** of their grant date. Miss the window and you owe
ordinary income tax on every vesting tranche for the next 4 years on
the spread between FMV and the price you paid.

Outputs:

1. **Deadline check** — postmark-by date + days remaining + urgency
   level (URGENT / NEAR / OK / EXPIRED), computed from your grant date.
2. **Election letter** — ready-to-print text following the model
   election from IRS Rev. Proc. 2012-29, with placeholders only where
   you must hand-fill (e.g. your TIN — the agent will not echo SSNs
   back to you).
3. **Mailing instructions** — the correct IRS service-center address
   for your state of residence (linked to the IRS lookup page for
   verification) and USPS certified-mail guidance.
4. **Calendar reminder** — a `.ics` file you can save and import to
   Google / Apple / Outlook calendar for the postmark deadline.
5. **Tax savings illustration** — using your actual numbers.
6. **Post-filing checklist** — what to keep, what to attach to next
   year's 1040, and where to update your cap table.

## Quick start

```bash
# CLI
python -m starter_business_agents.election_83b_agent.agent \
  "Founder Jane Doe at 123 Main St, Austin TX 78701. Issuer Acme Books Inc., \
   Delaware C-Corp, EIN 88-1234567. Granted 8,000,000 shares common stock \
   on 2026-05-01. FMV $0.0001/share, paid $0.0001/share. 4-year monthly \
   vesting with 1-year cliff."

# Streamlit UI (form inputs)
streamlit run starter_business_agents/election_83b_agent/app.py
```

## Tools the agent uses

- `eighty_three_b_deadline_check(grant_date)` — pure date math; returns
  the 30-day postmark deadline and an urgency level. No LLM-fabricated
  dates.
- `irs_service_center_for_state(state)` — table-based lookup; returns
  the IRS service-center address for paper Form 1040 routing (where
  §83(b) elections go) and the IRS lookup URL for verification.

Both tools are deterministic — no network calls, no LLM creativity in
the legally-binding parts.

## NOT legal or tax advice

The §83(b) election is **irrevocable** once filed. The output of this
agent is a draft, not a final filing. Have a CPA or tax attorney review
the letter before signing and mailing. Verify the IRS service-center
address on the IRS lookup page returned by the tool — addresses change.

## Customizing

- `prompts.py::SYSTEM_PROMPT` — change the output sections, urgency
  wording, or restriction descriptions.
- `tools.py::_STATE_TO_CENTER` — when the IRS updates routing (it
  happens), update the snapshot table here. The agent always links the
  IRS lookup URL so a stale snapshot won't silently mislead a founder.
