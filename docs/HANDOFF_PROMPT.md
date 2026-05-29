# Handoff Prompt — Keel verification, security review & agent interrogation

Copy everything in the fenced block below into a fresh **Claude Code**
session opened at the repo root (`ai-native-business-apps/`), logged into a
Claude Max/Pro subscription so the agents can actually run.

Context for you (not part of the prompt): a refactor just landed on branch
`claude/brave-knuth-Bp4Ed` that introduced the unified **Company** spine
(`core/company.py`), a **prepare-to-submit artifact** layer
(`core/artifacts.py`), shared utils (`core/util.py`), a **brand** layer
(`core/brand.py`), and the flagship **Founding Journey** orchestrator
(`advanced_business_agents/multi_agent_apps/founding_journey/`). It also
rebranded the product to **Keel** and added a launch kit under
`docs/launch/`. The pipeline is unit-tested offline with a fake LLM, but
**no live Claude run has been done yet**, and there has been **no security
review** and **no independent quality audit of the individual agents**.
That's your job.

---

```
You are auditing the "Keel" repo (an open-source AI back-office for founders;
the flagship is the Founding Journey orchestrator). A large refactor just
landed on this branch. Work through THREE missions in order and produce a
written report for each. Do not push changes to `main`. Make fixes on the
current feature branch and commit them with clear messages. Open NO pull
request unless I explicitly ask.

Start by reading: README.md, CLAUDE.md, core/company.py, core/artifacts.py,
core/util.py, core/cli.py, and the whole
advanced_business_agents/multi_agent_apps/founding_journey/ folder.

═══════════════════════════════════════════════════════════════════════
MISSION 1 — VERIFY THE WORK (does it actually run and do what it claims?)
═══════════════════════════════════════════════════════════════════════
1. Run the full test suite: `pip install -e . && pip install pytest ruff &&
   python -m pytest -q && ruff check .`. Report pass/fail verbatim. Fix any
   failures.
2. Verify imports of every new module and every agent: for each agent package
   run `python -c "from <pkg>.agent import run"`. List anything that breaks.
3. LIVE-RUN the Founding Journey end to end against Claude:
   `keel founding-journey --cli '{"legal_name":"Northwind Robotics, Inc.",
   "one_liner":"Warehouse robots","home_state":"California",
   "state_of_formation":"Delaware","entity_type":"C-Corp",
   "formation_date":"2026-06-01"}'`
   Confirm: all 5 steps run in order, the synthesis packet has every required
   section, and the context actually threads (does step 3's legal doc match
   the entity chosen in step 1?). Capture the output as a golden baseline under
   the agent's tests/baselines/ and update its PARITY.md "Last verified" row.
4. Generate and inspect the artifacts (write them to a temp dir via the
   Python API): confirm company.json round-trips, the .html is valid &
   printable, and the .ics imports (validate it against RFC 5545 — every
   VEVENT has DTSTAMP/UID/DTSTART, dates are correct, the 83(b) postmark =
   formation_date + 30 days).
5. Smoke-test that each Streamlit app at least imports/parses (don't need a
   browser): `python -c "import ast; ast.parse(open('<app.py>').read())"` and
   check the imports resolve.
DELIVERABLE: docs/audit/VERIFICATION.md — what works, what's broken, what you
fixed, and the captured baseline location.

═══════════════════════════════════════════════════════════════════════
MISSION 2 — SECURITY REVIEW
═══════════════════════════════════════════════════════════════════════
Run the /security-review skill on the diff of this branch vs main, then go
deeper on these Keel-specific surfaces:
  • Subscription guard (core/llm/claude.py::_enforce_subscription_guard): can a
    real API key leak through when the user expects subscription-only? Are the
    env whitelist markers (CLAUDECODE etc.) spoofable in a way that matters?
  • Secret handling: confirm no keys are logged, written into artifacts, or
    embedded in company.json. Grep the artifact builders.
  • Artifact write paths (core/artifacts.py, journey.build_artifacts): any path
    traversal via company.legal_name → slug → filename? Confirm slugify can't
    escape the output dir.
  • Injection into generated files: the .ics and .html builders take
    LLM/user text. Confirm .ics escaping (RFC 5545: `; , \ \n`) and HTML
    escaping are complete and can't break out of the document (CRLF injection
    into ICS, <script> into HTML).
  • Prompt-injection: a malicious "company description" is fed to 5 agents and a
    synthesizer. What's the blast radius? (No tools here exfiltrate, but
    confirm.) Note whether any agent's allowed_tools could be abused.
  • Dependency review: any new deps? (Should be none.) Check the install path.
DELIVERABLE: docs/audit/SECURITY.md — findings by severity (crit/high/med/low),
each with a repro and a fix. Apply the fixes you're confident in; flag the rest.

═══════════════════════════════════════════════════════════════════════
MISSION 3 — INTERROGATE EACH AGENT INDEPENDENTLY (virality & utility)
═══════════════════════════════════════════════════════════════════════
Spawn ONE sub-agent PER agent folder (14 total: 9 starter + 5 advanced), in
parallel, each doing a deep independent audit of just that one agent. Give each
sub-agent this rubric and have it score 1–5 and justify:
  • UTILITY: does it solve a real, painful, frequent founder problem? Would a
    founder actually use the output, or is it generic LLM filler?
  • CORRECTNESS: read prompts.py + tools.py. Are the legal/tax claims accurate
    and current (entity rules, 83(b) 30-day rule, DE franchise-tax APVC method,
    sales-tax nexus, worker-classification ABC test)? Flag anything wrong or
    dangerously oversimplified — this is the credibility moat.
  • PREPARE-TO-SUBMIT GAP: does it produce a real artifact, or just advice? If
    advice-only, what artifact SHOULD it emit (filled form, letter, checklist,
    .ics) and how hard is it to add via core/artifacts.py?
  • SPINE INTEGRATION: does it read from the shared Company profile? (Only
    business_license was refactored to use core.util; most agents still ask for
    facts independently.) Propose the change to have it accept Company context.
  • VIRALITY: is there a single shareable "wow" in this agent (a number, a
    saved fee, an averted disaster) that belongs in launch content? The
    delaware-franchise-tax "$85K→$400" and the 83(b) "30 days or it's gone"
    are the model.
Then YOU synthesize all 14 reports into one ranked table.
DELIVERABLE: docs/audit/AGENT_AUDIT.md — the ranked table (best→weakest agent
by utility×correctness), the top 5 correctness issues to fix before launch, and
the top 5 "wow" hooks for the launch content. File a GitHub issue for each
correctness bug (labeled `bug` / `good-first-issue` as appropriate) — but do
NOT post anything publicly beyond issues without my OK.

═══════════════════════════════════════════════════════════════════════
WRAP-UP
═══════════════════════════════════════════════════════════════════════
Commit your fixes and the three audit docs. Reply with a one-screen summary:
overall go/no-go for launch, the must-fix blockers, and the single highest-
leverage improvement you'd make next. Be blunt — I'd rather hear it's not ready
than ship something that burns a founder.
```
