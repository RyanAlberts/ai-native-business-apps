# Parity Report — Founding Journey

| | |
|---|---|
| Path | `advanced_business_agents/multi_agent_apps/founding_journey/` |
| Default model | claude-sonnet-4-6 |
| Pattern | Custom orchestrator over 5 starter agents + synthesis |
| Last verified | _pending live run — see Known gaps_ |

## 1. Capability parity

Reuses the underlying starter agents' tools (incorporation, 83(b), legal
docs, banking, compliance). The synthesis step uses no tools.

| Capability | claude | openai | gemini | xai | ollama | codex |
|---|---|---|---|---|---|---|
| 5-step threaded orchestration | ✅ (offline-tested) | ✅ | ✅ | ✅ | ✅ | ⏳ |
| Packet synthesis | ✅ (offline-tested) | working | working | community | community | ⏳ |
| Deterministic `.ics` deadlines | ✅ (unit-tested, provider-independent) | ✅ | ✅ | ✅ | ✅ | ✅ |

## 2. Behavioral parity

| ID | Prompt | claude | openai | gemini |
|---|---|---|---|---|
| g1 | Two-founder DE C-Corp SaaS, TX-based, seed in 9mo | ⏳ pending | — | — |
| g2 | Solo WY LLC e-commerce, bootstrapped | ⏳ pending | — | — |
| g3 | Robotics C-Corp, CA home / DE formation, hardware liability | ⏳ pending | — | — |

The full pipeline (ordering, context threading, synthesis, artifact
generation) is verified **offline** with a fake LLM in
`tests/test_journey.py` (8 tests). What remains is a live Claude run to
capture golden baselines.

## 3. UX parity

- [x] Single structured intake form (one profile, not five)
- [x] Live per-step progress (`st.progress` + `st.status`)
- [x] Final packet rendered, with per-specialist expander
- [x] Prepare-to-submit artifact downloads (md / html / .ics / company.json)

## 4. Known gaps

- **Live golden run pending.** The orchestration is offline-tested; a real
  Claude run to capture baselines is part of the handoff verification.
- `.ics` covers the deterministically-derivable deadlines (83(b) postmark,
  DE franchise tax). State annual-report dates without a fixed cadence are
  surfaced in the packet's narrative table, not the calendar.
- No EIN auto-application — the packet routes the founder to the IRS portal
  (prepare-to-submit, by design).

## 5. Verdict

| Provider | Verdict |
|---|---|
| claude | offline-verified; live baseline pending |
| openai | working (untested) |
| gemini | working (untested) |
| xai | community-supported |
| ollama | community-supported (32B+ recommended) |
| codex | stub |
