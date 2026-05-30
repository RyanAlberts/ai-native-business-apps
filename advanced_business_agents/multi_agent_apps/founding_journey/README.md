# 🚀 Founding Journey — the unified Day-0 back office

> Fill in your company **once**. Get a complete, ordered **Day-0 Formation
> Packet** — incorporation, 83(b), legal docs, banking, and a compliance
> calendar — plus the real files, ready to submit.

This is the flagship agent: the open-source answer to "Stripe Atlas, but
yours." Where the standalone agents each solve one task, the Founding
Journey threads a single shared [`Company`](../../../core/company.py)
profile through five specialists in the correct real-world order, then
synthesizes one coherent packet.

## What it does

```
company.json  ──►  🏛️ Incorporation
                   📬 83(b) Election        each step sees the company
                   📜 Founding Legal Docs   profile + every upstream
                   🏦 Banking & Insurance   decision
                   📋 Compliance & Tax
                        │
                        ▼
                   📦 Day-0 Formation Packet  (synthesis)
                        ├─ Master Day-0 checklist (correct ordering)
                        ├─ Key deadlines table
                        ├─ Deduplicated links & portals
                        └─ Documents prepared
```

## Prepare-to-submit artifacts

Every run produces real, downloadable files — not just advice:

| File | What it is |
|---|---|
| `company.json` | Your portable profile — re-loadable into any standalone agent. |
| `00-formation-packet.md` | The synthesized Day-0 packet (Markdown). |
| `00-formation-packet.html` | The same packet as a printable page → **Save as PDF**. |
| `NN-<step>.md` | Each specialist's full output, numbered in order. |
| `compliance-deadlines.ics` | Real calendar file (83(b) postmark, franchise tax) — import to Google/Apple/Outlook. |

The `.ics` deadlines are computed **deterministically** from your facts
(formation date, state, entity type) — never parsed out of LLM prose — so
they're trustworthy.

## Run it

```bash
keel founding-journey            # Streamlit UI (structured intake)
agent founding-journey           # same, via the legacy `agent` command
agent founding-journey --cli "Two-founder DE C-Corp SaaS, based in TX, raising a seed."
```

You can also start from a saved profile:

```bash
agent founding-journey --cli ./company.json
```

## How it's built

The journey **does not** call each agent's `run()` (which would spin up
five separate LLM clients). Instead it imports each agent's real
`SYSTEM_PROMPT` + `all_tools` and drives them with one shared
`LLMClient` — so the domain logic stays single-sourced and the whole
pipeline is unit-testable offline with a fake LLM (see
[`tests/test_journey.py`](tests/test_journey.py)).

See [WALKTHROUGH.md](WALKTHROUGH.md) for the narrative tour and
[PARITY.md](PARITY.md) for provider verification status.
