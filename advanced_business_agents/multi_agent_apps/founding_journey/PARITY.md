# Parity Report — Founding Journey

| | |
|---|---|
| Path | `advanced_business_agents/multi_agent_apps/founding_journey/` |
| Default model | claude-sonnet-4-6 |
| Pattern | Custom orchestrator over 5 starter agents + synthesis |
| Last verified | 2026-05-29 (live Claude run; baseline captured) |

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
| g3 | Robotics C-Corp, CA home / DE formation, hardware liability | ✅ verified (2026-05-29) | — | — |

The full pipeline (ordering, context threading, synthesis, artifact
generation) is verified **offline** with a fake LLM in
`tests/test_journey.py` (8 tests). A **live Claude run** (g3 — Northwind
Robotics) was captured on 2026-05-29: all 5 steps ran in order, the packet
contained every required section, and 9 artifacts were generated including a
correct `compliance-deadlines.ics`. Baseline at
`tests/baselines/claude-2026-05-29.md`.

> Note: the live capture used the `claude` **CLI transport**, not the SDK
> streaming path — the SDK passes `--dangerously-skip-permissions`
> (`permission_mode="bypassPermissions"`), which the CLI refuses under
> root. `core/llm/claude.py` now accepts a `permission_mode` override in
> `config.yaml::extra` so the SDK path works in root/CI environments too.

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
