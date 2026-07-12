# Founding Journey — Progress

Live status of this founding journey. The AI agent updates this file the
moment each phase's gate passes — it's how any fresh session knows exactly
where things stand. (Founder: you never need to edit this, but it's yours
to read any time.)

Running the journey through the Python CLI instead? This file only tracks
the agent-native path (`playbooks/`) — the CLI runs all phases in one go.

## Phase status

| Phase | What | Status | Date | Notes |
|---|---|---|---|---|
| 00 | Interview → `company.json` | Not started | — | — |
| 01 | Incorporation (entity, state, filing plan) | Not started | — | — |
| 02 | 83(b) election letter + deadline | Not started | — | — |
| 03 | Founding legal documents | Not started | — | — |
| 04 | Banking & insurance plan | Not started | — | — |
| 05 | Compliance & tax calendar | Not started | — | — |
| 06 | Day-0 Formation Packet (synthesis) | Not started | — | — |

Status values: `Not started` → `In progress` → `Done` (gate passed). A
phase completed with a known gap is `Done (gap: …)`. If something that was
Done breaks later, it goes back to `BROKEN — fix first`.

## Company summary

*(Filled in after the Phase 00 interview: what the company is, who the
founders are, entity and state once decided.)*

## Phase notes

*(The agent adds a dated entry here as each phase completes: decisions
made, deadlines computed, anything deferred and who owns it.)*

## How to resume

1. Open this folder with your AI agent (Claude Code, Codex, Cursor, …) and
   say **"continue my founding journey"**.
2. The agent re-reads this file and `company.json`, runs
   `bash verify/journey_gate.sh all`, and continues at the first phase
   that's broken or not started.
