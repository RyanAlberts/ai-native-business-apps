# Worker Classification Agent — 1099 vs W-2

**What LegalZoom sells**: employment + IC contract templates (template-only;
no decision support).
**What PEOs (Gusto/Rippling/Justworks) sell**: classification advisory as
part of their HRIS platforms ($40–$80/employee/month).
**What employment attorneys charge**: $500–$1,500 for a classification
review.
**What this agent charges**: $0. Open source.

## The pain

Misclassification is one of the most common and expensive payroll
mistakes founders make. A finding in an IRS or state audit can mean back
payroll-tax assessments going back multiple years, plus state penalties
(California: up to $25K per worker; New Jersey: $2,500 first-offense
civil per worker; etc.).

The founder mistake everyone makes: treating a full-time role as 1099 to
avoid payroll burden. Calling someone an "independent contractor" in a
contract DOES NOT make them one. Courts and agencies look at the actual
working relationship.

## What it does

Applies three layered tests:

1. **IRS three-category common-law test** — behavioral control,
   financial control, relationship of the parties.
2. **DOL six-factor economic-reality test** (2024 Final Rule, effective
   March 11, 2024) — for FLSA wage-and-hour classification. Note: the DOL
   announced in 2025 (FAB 2025-1) that it is not currently enforcing this
   rule, so the agent treats it as an analytical framework rather than
   actively-enforced policy.
3. **State-specific overrides** — California ABC test (AB5),
   Massachusetts ABC test, New Jersey ABC test, Illinois ABC test
   (construction), New York Freelance Isn't Free Act.

In ABC-test states, **failing ANY of A/B/C forces W-2 regardless of how
the federal factors lean**. The agent surfaces this front-and-center.

Outputs:
- **Verdict**: W-2 / 1099 / HIGH RISK.
- **Risk score**: LOW / MEDIUM / HIGH.
- **State framework analysis** — walk through A, B, C if applicable.
- **IRS three-category analysis** — per-category lean + reasoning.
- **DOL six-factor table** — factor × lean × why.
- **Recommendation** — including which contract type to issue (with a
  pointer to `legal_doc_agent` for the actual contract).
- **If borderline**: 2-3 structural changes that would push the
  relationship one direction or the other.
- **Cost of misclassification** — quantified when relevant.
- **Common founder mistakes** — including the "we have an IC agreement
  so we're safe" myth and the "they want to be 1099" myth.

## Quick start

```bash
# CLI
python -m starter_business_agents.worker_classification_agent.agent \
  "Role: lead engineer. Full-time 9-5 in our office. Company laptop. \
   Hourly at \$150/hr. No benefits. We want to call them 1099."

# Streamlit UI (structured form)
streamlit run starter_business_agents/worker_classification_agent/app.py
```

## Tools

- `classification_tests_reference()` — returns the canonical IRS three-
  category factor list and DOL 2024 six-factor list with source URLs.
  Pure reference data — no LLM-invented factor names.
- `state_classification_law_lookup(state)` — returns the governing
  framework (ABC test in CA/MA/NJ; common-law elsewhere) + failure rule
  + source URL.

## NOT legal advice

Worker classification is fact-specific and audit-sensitive. The agent's
output is a structured starting point you must validate with:

- An employment attorney licensed in the state where the work will be
  performed, OR
- A PEO/HRIS provider (Gusto, Rippling, Justworks, TriNet) that takes
  on co-employment liability and stakes their reputation on the
  classification.

## Sources

- IRS classification guidance: https://www.irs.gov/businesses/small-businesses-self-employed/independent-contractor-self-employed-or-employee
- DOL 2024 Final Rule: https://www.dol.gov/agencies/whd/flsa/misclassification/rulemaking
- California AB5: https://www.dir.ca.gov/dlse/faq_independentcontractor.htm
- Massachusetts ABC test: https://www.mass.gov/info-details/independent-contractor-laws-and-regulations
- New Jersey: https://www.nj.gov/labor/employer-services/business/classification.shtml
- NY Freelance Isn't Free Act: https://www.ny.gov/programs/freelance-isnt-free-act
