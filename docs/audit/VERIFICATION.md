# Mission 1 — Verification Report

_Audit of branch `claude/cool-ramanujan-bD7zK` (post-Keel-refactor). Date: 2026-05-30._

This report records whether the refactored code **runs and does what it claims**.
Scope: full test suite, import surface, a live Claude run of the Founding
Journey, artifact validation, and a Streamlit smoke test.

## TL;DR

| Check | Result |
|---|---|
| `pytest` | ✅ **74 passed** (was 73; +1 regression test added by this audit) |
| `ruff check .` | ✅ clean |
| Import every new module + all 14 agents | ✅ all import |
| Live Claude run of Founding Journey | ⚠️ **partial** — steps 1–2 run & thread correctly; step 3 (legal docs) errored once and was very slow on retry (see below) |
| Artifact layer (company.json / HTML / ICS / 83(b) math / slug safety) | ✅ all pass after **1 fix** (ICS CRLF escaping) |
| Streamlit apps parse + imports resolve | ✅ all 14 |

**Bottom line:** the offline product is solid and well-tested. The *live*
orchestrator is fragile: a single flaky step kills the entire run with no
partial-result recovery. That is the headline gap for Mission 1.

---

## 1. Test suite & lint

```
$ pip install -e . && python -m pytest -q
74 passed in ~0.2s
$ ruff check .
All checks passed!
```

No failures to fix. The suite is fast and offline (fake LLM). I **added one
regression test** — `core/tests/test_artifacts.py::test_ics_neutralizes_crlf_injection`
— covering the ICS escaping bug found in Mission 2 (see SECURITY.md).

## 2. Import surface

Every new core module (`core.company`, `core.artifacts`, `core.util`,
`core.brand`) and **all 14 agents** import cleanly:

```
for pkg in <9 starter + 5 advanced>; do python -c "from ${pkg}.agent import run"; done
→ OK for all 14
```

Nothing broken.

## 3. Live Claude run — Founding Journey (⚠️ partial)

Environment note: this container runs as **root**, and the Claude Agent SDK
passes `--dangerously-skip-permissions`, which the CLI refuses under root. The
shipped `founding_journey/config.yaml` has **no `permission_mode` override**, so
a root/CI live run fails immediately unless `extra.permission_mode: default` is
injected. I injected it at runtime (did not mutate the shipped config).
**Recommendation:** document this in the agent README or default the config to
`default` so CI/root containers work out of the box.

Input (per the audit brief):
```json
{"legal_name":"Northwind Robotics, Inc.","one_liner":"Warehouse robots",
 "home_state":"California","state_of_formation":"Delaware",
 "entity_type":"C-Corp","formation_date":"2026-06-01"}
```

**What worked (verified live against Claude):**
- Step 1 — Incorporation: produced a full filing plan (~17–21k chars).
- Step 2 — 83(b): ran *after* step 1 and **the context threaded** — step 2's
  output reflected the C-Corp/Delaware decision from step 1 (it did not re-ask).
  This confirms the spine + transcript threading work on a real model.

**What broke / stalled at step 3 (Legal Docs):**
- Run 1: aborted with `Exception: Claude Code returned an error result: success`
  raised from `claude_agent_sdk` inside `ClaudeClient.complete()`.
- Run 2: did **not** reproduce the error — step 3 was simply **very slow** (the
  legal-doc step generates multiple long documents; its `claude` subprocess was
  still generating after several minutes and I stopped the run to finalize).
- So the failure is **intermittent**, not deterministic; the legal-doc step is
  the slow/fragile link (likely brushing `max_tokens` 8192 / `max_turns` 12, or
  an SDK result-subtype edge case under load).
- **Critical robustness finding:** `run_journey()` has **no try/except around
  the per-step `llm.complete()` call** (`journey.py:147`). One failed step
  raises straight out of the loop, discarding the successful upstream steps and
  producing **no packet and no artifacts**. A founder would see a stack trace,
  not a partial result.

**Recommended fix (flagged, not applied — needs a design choice):** wrap each
step in try/except, record a `StepResult` with an error marker, continue the
journey, and let the synthesis step note the gap. That converts a hard crash
into a degraded-but-useful packet.

**Baseline:** because the end-to-end run did not complete, no full golden
baseline was captured under `tests/baselines/`. Steps 1–2 transcripts and the
run log are preserved at `/tmp/journey_run*.log` for this session. PARITY.md was
therefore **not** marked "verified end-to-end" — doing so would misrepresent
what actually ran (the repo's own convention: _"mark verified only after
running it"_).

## 4. Artifact validation (✅ after 1 fix)

Built the artifact set from the Northwind profile via the Python API and
validated against RFC 5545 and the spec in the brief
(`scripts/_validate_artifacts.py`, a throwaway harness — not committed):

- ✅ `company.json` round-trips (`Company.from_json(...).to_dict() == original`).
- ✅ HTML is self-contained & printable (`<!doctype html>`, `@page` + `@media print`).
- ✅ ICS: `BEGIN/END:VCALENDAR`, CRLF line endings, every VEVENT has
  `UID` + `DTSTAMP` + `DTSTART`.
- ✅ **83(b) postmark = formation_date + 30 days**: formation `2026-06-01` →
  postmark `2026-07-01`, present in the ICS as `20260701`.
- ✅ Delaware franchise-tax VEVENT present for a DE C-Corp.
- ✅ Slug safety: `legal_name = "../../../../etc/passwd"` cannot escape the
  output dir (filenames are hardcoded constants; the slug is never a path).
- ✅ HTML escaping: `<script>` in packet body and title is escaped.
- 🔧 **ICS CRLF injection — FIXED.** `core/artifacts.py::_ics_escape` escaped
  `\ ; , \n` but **not raw `\r`**. A carriage return in any LLM/user text
  survived into the file as a raw control char (malformed per RFC 5545 §3.1 and
  a calendar-injection vector). Fixed to normalize CRLF/CR/LF → escaped `\n`.
  See SECURITY.md for the repro.

Separately, I confirmed the **DE franchise-tax date bug** in
`journey.deadlines_for()` and **fixed it** (it computed `today.year + 1`
unconditionally, skipping an imminent March 1 for anyone viewing Jan 1–Mar 1).
Verified: viewed 2027-02-15 now yields `2027-03-01`, not `2028-03-01`.

## 5. Streamlit smoke test (✅)

All 14 `app.py` files parse (`ast.parse`) and their imports resolve. Not run in
a browser (headless container), but no import/syntax breakage.

## Fixes applied in Mission 1

1. `core/artifacts.py` — ICS `\r` escaping (RFC 5545 / injection hardening).
2. `advanced_business_agents/.../founding_journey/journey.py` — franchise-tax
   year bug.
3. `core/tests/test_artifacts.py` — added ICS CRLF-injection regression test.

## Still open (not fixed here)

- **Per-step error resilience in `run_journey()`** (highest-priority robustness
  gap — needs a design decision on partial-result semantics).
- **Live end-to-end baseline** not captured (blocked by the step-3 abort).
- Default `permission_mode` so root/CI live runs work without manual injection.
