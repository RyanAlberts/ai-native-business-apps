# Mission 3 — Per-Agent Interrogation & Synthesis

_Branch `claude/cool-ramanujan-bD7zK`. Date: 2026-05-30._

Each of the 14 agents (9 starter + 5 advanced) was independently audited by a
dedicated sub-agent against a 5-axis rubric (1–5): **Utility, Correctness,
Prepare-to-submit, Spine integration, Virality**. Below is the synthesized
ranking, the must-fix correctness issues (legal facts independently
re-verified against primary sources where time-sensitive), and the launch
hooks.

## Ranked table (best → weakest by Utility × Correctness)

| Rank | Agent | U | C | P2S | Spine | Viral | U×C | Verdict |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|---|
| 1 | **legal_doc** | 5 | 4 | 4 | 2 | 5 | 20 | fix-then-ship |
| 2 | **supplier_sourcing** | 5 | 4 | 4 | 2 | 4 | 20 | fix-then-ship |
| 3 | **delaware_franchise_tax** | 5 | 4 | 2 | 2 | 5 | 20 | fix-then-ship |
| 4 | **incorporation** | 5 | 4 | 2 | 2 | 4 | 20 | fix-then-ship |
| 5 | **bank_insurance** | 4 | 4 | 2 | 3 | 3 | 16 | fix-then-ship |
| 6 | **election_83b** | 5 | 3 | 2 | 2 | 5 | 15 | fix-then-ship |
| 7 | **trademark_search** | 5 | 3 | 4 | 1 | 4 | 15 | fix-then-ship |
| 8 | **business_license** | 5 | 3 | 2 | 2 | 4 | 15 | fix-then-ship |
| 9 | **loan_application** | 4 | 3 | 2 | 1 | 3 | 12 | fix-then-ship |
| 10 | **website_launch** | 4 | 3 | 2 | 1 | 4 | 12 | fix-then-ship |
| 11 | **worker_classification** | 5 | 2 | 2 | 1 | 4 | 10 | fix-then-ship |
| 12 | **compliance_tax** | 5 | 2 | 4 | 1 | 4 | 10 | fix-then-ship |
| 13 | **business_plan** | 3 | 3 | 2 | 1 | 3 | 9 | fix-then-ship |
| 14 | **founding_journey** ⭐ | 4 | 2 | 3 | 4 | 4 | 8 | fix-then-ship |

(P2S = prepare-to-submit score.) ⭐ = flagship. Note founding_journey ranks last
on U×C purely because of **fixable orchestration bugs** (one already fixed); its
spine integration is the best in the repo (4/5) and it's the product's
centerpiece — read its verdict, not just its rank.

### Cross-cutting themes
- **Utility is genuinely high** (mean ~4.6). These solve real, expensive,
  frequent founder problems — not LLM filler. The competitive framing ("$0 vs.
  LegalZoom/Stripe Atlas/Carta") is consistently true.
- **Spine integration is the systemic weakness** (mean ~1.9). Only
  `business_license` (via `core.util`) and `founding_journey` (the consumer)
  touch the `Company` spine. **Every** standalone `run()` takes a free-text
  string and re-asks for facts the profile already holds. The fix is the same
  ~5-line change everywhere: accept `run(input: str | Company)`, and if a
  `Company` is passed, prepend `company.to_context()`. This is the single
  highest-leverage repo-wide improvement.
- **Prepare-to-submit is half-built.** `core/artifacts.py` ships `ics_artifact`,
  `html_artifact`, `letter_html` — but most agents return raw markdown and never
  call them. The agents that *do* emit structured artifacts (compliance_tax ICS,
  trademark TEAS pre-fill, supplier RFP, legal_doc drafts) score notably higher.

---

## Top 5 correctness issues to fix BEFORE launch

These are credibility-critical — they're wrong *legal/tax facts* a founder would
act on. Time-sensitive claims were re-verified against primary sources.

### 1. 🔴 CRITICAL — Beneficial Ownership (BOI / Corporate Transparency Act) is stated as a live obligation; **domestic companies are now exempt**
Affects **incorporation**, **compliance_tax**, and **loan_application**.
- incorporation says _"File a BOI report with FinCEN within 90 days of formation."_
- compliance_tax says _"BOI is high-stakes ($500/day penalties) — always mention it"_ and lists it as a mandatory calendar event.
- **Reality:** FinCEN's interim final rule (published **March 26, 2025**) removed
  BOI reporting for **all U.S.-created entities** — "domestic reporting
  companies" and their beneficial owners are **exempt**. Only foreign reporting
  companies registered to do business in the U.S. must file.
  ([FinCEN](https://www.fincen.gov/news/news-releases/fincen-removes-beneficial-ownership-reporting-requirements-us-companies-and-us),
  [Federal Register 2025-05199](https://www.federalregister.gov/documents/2025/03/26/2025-05199/beneficial-ownership-information-reporting-requirement-revision-and-deadline-extension),
  [Treasury](https://home.treasury.gov/news/press-releases/sb0060))
- Both the agents' framing **and** a tempting "fix it to 30 days" are wrong for a
  U.S. LLC/Corp today. Telling founders to file an exempt report, or scaring
  them with $500/day penalties on a non-obligation, is exactly the credibility
  failure that sinks a legal-adjacent tool. **Fix:** scope BOI to foreign
  reporting companies only; for domestic entities, state they're exempt under
  the 2025 IFR (and note the rule is being finalized — re-verify before launch).

### 2. 🟠 HIGH — Worker classification cites a non-enforced rule as current law + unsourced statistics
Affects **worker_classification** (and the DOL framing in **compliance_tax**).
- Presents the _"DOL 2024 Final Rule (effective March 11, 2024)"_ six-factor
  economic-reality test as operative enforcement law.
- **Reality:** DOL Field Assistance Bulletin **2025-1 (May 1, 2025)** instructs
  staff to **stop applying** the 2024 rule and revert to the 2008 Fact Sheet #13
  framework; the rule survives only for private litigation and DOL intends to
  rescind it.
  ([DOL FAB 2025-1](https://www.dol.gov/sites/dolgov/files/WHD/fab/fab2025-1.pdf),
  [Jackson Lewis](https://www.jacksonlewis.com/insights/businesses-get-break-dol-wont-enforce-2024-independent-contractor-rule))
- Plus two **unsourced statistics** repeated across `agent.py`/`prompts.py`/
  `README.md`: _"roughly 40% of small businesses receive a payroll-
  misclassification finding"_ and _"avg $845 in penalties."_ Neither traces to
  IRS/DOL data. **Fix:** add a "DOL is not currently enforcing the 2024 rule"
  caveat; remove or cite the statistics; add Form SS-8 to the output.

### 3. 🟠 HIGH — 83(b) instructs founders to "attach the election to your Form 1040"
Affects **election_83b** (`prompts.py` mailing instructions + post-filing steps).
- Labeled _"current IRS instructions."_
- **Reality:** Treasury Decision **9779 (2016)** eliminated the requirement to
  attach the 83(b) election to the taxpayer's return for transfers on/after
  Jan 1, 2015. You must still file within 30 days and **keep a copy**. **Fix:**
  "Keep a copy permanently; attaching to the return is no longer required."
  (The 30-day deadline, certified-mail, and Form 15620 e-file guidance are
  correct.)

### 4. 🟡 MEDIUM — business_license gives wrong DBA jurisdiction for two states + a stale agency URL
Affects **business_license** (`tools.py` jurisdiction table).
- **AZ** `level="county"` — Arizona has **no mandatory** DBA for LLCs/corps at
  any level; founders are told to file with a county clerk that doesn't require
  it.
- **NJ** `level="state+county"` — for an **LLC**, alternate-name registration is
  **state-only**; the county step applies to sole proprietors/partnerships.
- **DC** DBA URL points at the retired `dcra.dc.gov` (renamed DLCP in 2021);
  `state_portals.py` already uses `dlcp.dc.gov` — an internal inconsistency.
- **Fix:** correct the AZ/NJ levels (ideally entity-type-aware), update the DC
  URL, and have the DBA tool delegate to `state_portals.py` rather than keep a
  second URL table.

### 5. 🟡 MEDIUM — founding_journey orchestration bugs (one fixed) + Delaware/EIN gaps
Affects **founding_journey** (`journey.py`).
- ✅ **FIXED:** `deadlines_for()` computed `today.year + 1` unconditionally,
  skipping the imminent March 1 Delaware deadline for anyone viewing Jan 1–Mar 1.
- **DE LLC franchise tax omitted:** the calendar only fires for `corp`; a DE LLC
  owes a **flat $300 due June 1** — no event is generated.
- **EIN gap:** the 83(b) and banking steps both require/assume an EIN, the
  synthesis prompt asserts _"you cannot open a bank account before the EIN,"_ but
  there is **no EIN step** and `Company.ein` is never collected or populated —
  so the 83(b) letter emits an `[EIN]` placeholder.
- **83(b) before legal docs:** step 2 (83b) runs before step 3 (legal docs that
  authorize the stock issuance the 83(b) covers). Debatable (both are drafts and
  83(b) urgency argues for surfacing early), but worth a deliberate decision.
- **"Save-as-PDF" HTML renders markdown literally:** `letter_html` only splits
  paragraphs + escapes, so `## headers`, `| tables |`, and `- [ ]` checkboxes
  appear as raw text in the printable packet — undercutting the "real files,
  ready to submit" claim. Needs a markdown→HTML pass.

_Honorable mention:_ **trademark_search** under-reports year-10 maintenance cost
(~$200/class) by including a Section 8 fee but **omitting the separate Section 9
renewal**, and conflates "freedom-to-operate" (a patent concept) with trademark
clearance without correcting the user.

---

## Top 5 "wow" hooks for launch content

1. **Delaware franchise tax: `$85,165 → $400`.** _(delaware_franchise_tax)_ The
   arithmetic is independently verified correct (Authorized-Shares vs. Assumed
   Par Value Capital). "Carta charges to fix it. This does it free in 30
   seconds." The single strongest, most-screenshotable number in the repo.
2. **83(b): "30 days or it's gone — forever."** _(election_83b)_ Pair the
   countdown with a ready-to-mail letter + certified-mail steps + a calendar
   reminder. "What LegalZoom doesn't sell and Stripe Atlas bundles into a $500
   formation — for $0."
3. **Dead equity: "A cofounder who quits on day 60 with no vesting keeps 50%
   forever — and it kills your Series A."** _(legal_doc)_ Plus the IP-assignment
   gotcha: "without it, your company may not own its own code." Visceral and
   true.
4. **Founding Journey: "One profile → a complete Day-0 packet — master
   checklist, deadlines, founding docs, 83(b) letter, and a calendar file that
   drops into Google Calendar. The open-source answer to Stripe Atlas."**
   _(founding_journey)_ The `.ics`-into-your-calendar moment is the tactile
   proof. (Fix the printable-HTML rendering first so the demo doesn't show raw
   markdown.)
5. **Trademark clearance: "Four agents fan out across USPTO + 50 state registries
   + live web + Nice classes → a GO / CAUTION / NO-GO verdict and a
   copy-pasteable TEAS pre-fill. Replaces a $899 LegalZoom package for $0."**
   _(trademark_search)_ — with the honest disclaimer that it's research, not a
   registrability opinion.

---

## Method note / caveat

Per-agent scores come from 14 independent Sonnet sub-agents reading each folder's
`prompts.py`/`tools.py`/`agent.py`/`README`. The **time-sensitive legal claims**
in the Top-5 (BOI/CTA, DOL IC rule) were **re-verified by me against primary
sources** (FinCEN, Federal Register, Treasury, DOL) — cited inline. The 83(b)
TD-9779 point and the franchise-tax/jurisdiction items are well-established and
checked against the code. **All legal/tax content should still get a
professional review before launch** — that is the credibility moat, and right
now three agents are shipping stale federal guidance.
