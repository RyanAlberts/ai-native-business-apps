# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tools for the Worker Classification Agent.

Two deterministic reference tools — they return real, citeable facts the
LLM uses to structure its analysis. The actual verdict comes from the
LLM applying the tests to the founder's situation, but the tests
themselves are not invented.

  * `classification_tests_reference` — canonical list of the IRS three-
    category common-law test factors + the DOL 2024 economic-reality
    test factors. Both source URLs included.

  * `state_classification_law_lookup` — given a state, returns the
    governing classification framework (ABC test states are MUCH stricter
    than the federal default), the failure threshold, and the official
    source URL.
"""
from __future__ import annotations

from core import Tool


_IRS_URL = (
    "https://www.irs.gov/businesses/small-businesses-self-employed/"
    "independent-contractor-self-employed-or-employee"
)
_DOL_2024_URL = (
    "https://www.dol.gov/agencies/whd/flsa/misclassification/rulemaking"
)
_CA_AB5_URL = "https://www.dir.ca.gov/dlse/faq_independentcontractor.htm"
_MA_URL = "https://www.mass.gov/info-details/independent-contractor-laws-and-regulations"
_NJ_URL = "https://www.nj.gov/labor/employer-services/business/classification.shtml"
_IL_URL = "https://labor.illinois.gov/laws-rules/conmed/employee-misclassification.html"
_NY_FIFA_URL = "https://www.ny.gov/programs/freelance-isnt-free-act"


_IRS_THREE_CATEGORIES = [
    {
        "category": "Behavioral control",
        "asks": (
            "Does the company control or have the right to control WHAT the "
            "worker does and HOW the worker does the job?"
        ),
        "factors": [
            "Type/degree of instructions given (when, where, what tools, what order)",
            "Training the company provides on how to do the work",
            "Evaluation systems that measure HOW the work is done (vs. just outcome)",
        ],
        "leans_w2_if": "company gives detailed instructions, trains the worker, or evaluates process",
        "leans_1099_if": "worker decides their own methods, tools, schedule, and process",
    },
    {
        "category": "Financial control",
        "asks": (
            "Does the company control the financial aspects of the worker's job?"
        ),
        "factors": [
            "Significant unreimbursed business expenses borne by the worker",
            "Worker's investment in their own equipment and facilities",
            "Worker's services available to the broader market (not just this company)",
            "Method of payment (hourly/weekly = W-2-leaning; flat fee per project = 1099-leaning)",
            "Worker can realize a profit or loss",
        ],
        "leans_w2_if": "fixed hourly/salary pay, no investment by worker, no other clients",
        "leans_1099_if": "flat-fee project pay, worker owns equipment, has other clients, bears expenses",
    },
    {
        "category": "Relationship of the parties",
        "asks": "How do the parties perceive their relationship?",
        "factors": [
            "Written contract describing the relationship (helpful but NOT determinative)",
            "Benefits provided (health insurance, PTO, retirement) — strong W-2 signal",
            "Permanency of the relationship (open-ended = W-2; project-bounded = 1099)",
            "Services performed are a key activity of the regular business (W-2 signal)",
        ],
        "leans_w2_if": "ongoing relationship, worker does core business activity, benefits provided",
        "leans_1099_if": "project-bounded, peripheral activity, no benefits",
    },
]


_DOL_2024_ECONOMIC_REALITY_FACTORS = [
    {
        "factor": "Opportunity for profit or loss",
        "asks": "Does the worker have meaningful opportunity for profit or loss based on managerial skill?",
        "leans_w2_if": "worker can't increase earnings through managerial decisions",
        "leans_1099_if": "worker bids work, accepts/declines jobs, hires helpers, advertises",
    },
    {
        "factor": "Investments by worker and employer",
        "asks": "Are the worker's investments capital or entrepreneurial in nature, separate from the employer's?",
        "leans_w2_if": "employer provides equipment, software, workspace",
        "leans_1099_if": "worker invests in their own tools, vehicle, software licenses",
    },
    {
        "factor": "Permanence of the work relationship",
        "asks": "Is the relationship indefinite/continuous (W-2) or project-based/sporadic (1099)?",
        "leans_w2_if": "open-ended engagement, full-time hours",
        "leans_1099_if": "fixed-term, project-specific, intermittent",
    },
    {
        "factor": "Nature and degree of control",
        "asks": "Who controls the work (scheduling, supervision, prices, ability to work for others)?",
        "leans_w2_if": "employer sets schedule, supervises, restricts other work",
        "leans_1099_if": "worker sets schedule, works unsupervised, free to work for competitors",
    },
    {
        "factor": "Whether work is integral to the employer's business",
        "asks": "Is the work performed integral to the company's business?",
        "leans_w2_if": "work IS the company's core product/service",
        "leans_1099_if": "work is ancillary (accounting for a software company; designer for a manufacturer)",
    },
    {
        "factor": "Skill and initiative",
        "asks": "Does the worker use specialized skills in connection with business-like initiative?",
        "leans_w2_if": "skills provided by employer training; worker has no separate business",
        "leans_1099_if": "worker brings specialized skills and exercises business judgment",
    },
]


def _classification_tests_reference(_args: dict) -> dict:
    """Return the canonical IRS + DOL test factor lists with source URLs."""
    return {
        "ok": True,
        "irs_three_category_test": {
            "source_url": _IRS_URL,
            "summary": (
                "The IRS replaced its older 20-factor test with three broad "
                "categories: behavioral control, financial control, and "
                "relationship of the parties. No single factor controls; "
                "the entire relationship is weighed."
            ),
            "categories": _IRS_THREE_CATEGORIES,
        },
        "dol_2024_economic_reality_test": {
            "source_url": _DOL_2024_URL,
            "effective": "March 11, 2024",
            "summary": (
                "DOL Final Rule restored the traditional six-factor "
                "economic-reality test for FLSA (wage-and-hour) "
                "classification. Totality-of-the-circumstances analysis, "
                "no single factor controls."
            ),
            "factors": _DOL_2024_ECONOMIC_REALITY_FACTORS,
        },
        "note": (
            "These are the FEDERAL frameworks. Many states impose stricter "
            "tests (esp. ABC test states). Always call "
            "state_classification_law_lookup(state) too."
        ),
    }


CLASSIFICATION_TESTS_REFERENCE = Tool(
    name="classification_tests_reference",
    description=(
        "Return the canonical factor lists for the IRS three-category "
        "common-law test (behavioral control, financial control, "
        "relationship) and the DOL 2024 six-factor economic-reality test. "
        "Each factor includes what it asks, what leans W-2, and what leans "
        "1099. Call this FIRST in every analysis so the factors come from "
        "the actual federal frameworks, not the model's recollection."
    ),
    input_schema={"type": "object", "properties": {}, "required": []},
    handler=_classification_tests_reference,
)


# State-specific frameworks. ABC test states are dramatically stricter
# than the federal common-law test — failing ANY of A, B, or C → W-2.
_STATE_LAWS: dict[str, dict] = {
    "CA": {
        "framework": "ABC test (AB5)",
        "description": (
            "California ABC test under AB5 (codified at Labor Code §2775). "
            "Worker is presumed an employee unless ALL THREE of A, B, and C "
            "are satisfied:"
            "\n  A. Free from the hiring entity's control and direction;"
            "\n  B. Performs work outside the usual course of the hiring "
            "entity's business; AND"
            "\n  C. Customarily engaged in an independently established "
            "trade, occupation, or business of the same nature as the work."
        ),
        "failure_rule": "FAIL ANY of A/B/C → W-2 employee (not contractor).",
        "key_exemptions": (
            "Specified occupations carved out (lawyers, accountants, "
            "physicians, certain creative professionals, real estate "
            "agents, etc.). Check current AB5 exemption list."
        ),
        "source_url": _CA_AB5_URL,
    },
    "MA": {
        "framework": "ABC test (M.G.L. c.149 §148B)",
        "description": (
            "Massachusetts ABC test — among the strictest in the US, "
            "predating AB5. Same A/B/C structure: control, outside usual "
            "course, customarily engaged in an independent business."
        ),
        "failure_rule": "FAIL ANY of A/B/C → W-2 employee.",
        "source_url": _MA_URL,
    },
    "NJ": {
        "framework": "ABC test",
        "description": (
            "New Jersey ABC test. A/B/C structure. Aggressive enforcement "
            "by NJ Dept of Labor since 2020."
        ),
        "failure_rule": "FAIL ANY of A/B/C → W-2 employee.",
        "source_url": _NJ_URL,
    },
    "IL": {
        "framework": "ABC test (Illinois Employee Classification Act, "
                     "construction industry; general common-law test for others)",
        "description": (
            "Illinois ABC test applies to construction by statute. Other "
            "industries use the federal common-law test, but IL DOL is "
            "aggressive on misclassification audits."
        ),
        "failure_rule": "Construction: FAIL ANY of A/B/C → W-2.",
        "source_url": _IL_URL,
    },
    "NY": {
        "framework": "Federal common-law test + Freelance Isn't Free Act",
        "description": (
            "NY uses the federal common-law test for classification, but "
            "the Freelance Isn't Free Act (statewide as of 2024) adds "
            "specific protections for freelancers: written contracts "
            "required at $800+/year per client, 30-day payment terms, "
            "double-damages for non-payment, retaliation prohibited."
        ),
        "failure_rule": "Misclassification audited under common-law test; "
                        "FIFA imposes additional written-contract / "
                        "payment requirements regardless of classification.",
        "source_url": _NY_FIFA_URL,
    },
}

_DEFAULT_LAW = {
    "framework": "Federal common-law test (IRS three-category) + DOL 2024 economic-reality test",
    "description": (
        "Most states default to the federal common-law / economic-reality "
        "frameworks. State unemployment and workers'-comp agencies often "
        "apply their own tests in audits — verify with state DOL before "
        "relying on this default."
    ),
    "failure_rule": "Totality-of-the-circumstances analysis under federal frameworks.",
    "source_url": _IRS_URL,
}


def _state_classification_law_lookup(args: dict) -> dict:
    state = (args.get("state") or "").strip().upper()
    if not state:
        return {"ok": False, "error": "state is required (2-letter code)."}
    aliases = {
        "CALIFORNIA": "CA",
        "MASSACHUSETTS": "MA",
        "NEW JERSEY": "NJ",
        "NEW YORK": "NY",
        "ILLINOIS": "IL",
    }
    state = aliases.get(state, state)

    if state in _STATE_LAWS:
        law = dict(_STATE_LAWS[state])
        law["state"] = state
        law["is_stricter_than_federal"] = law["framework"].startswith("ABC")
        law["ok"] = True
        return law
    return {
        "ok": True,
        "state": state,
        **_DEFAULT_LAW,
        "is_stricter_than_federal": False,
        "verify_note": (
            f"No special state-level framework on file for {state}. The "
            "agent defaults to the federal frameworks; verify with this "
            "state's DOL site that no stricter test applies."
        ),
    }


STATE_CLASSIFICATION_LAW_LOOKUP = Tool(
    name="state_classification_law_lookup",
    description=(
        "Return the worker-classification legal framework for a US state. "
        "Critical because ABC-test states (CA, MA, NJ, parts of IL) are "
        "MUCH stricter than the federal common-law test — failing ANY of "
        "the A/B/C prongs forces W-2 classification. Always call this for "
        "the state where the worker will perform the work."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "state": {
                "type": "string",
                "description": "US state — 2-letter code (e.g. 'CA', 'TX') or full name.",
            },
        },
        "required": ["state"],
    },
    handler=_state_classification_law_lookup,
)


def all_tools() -> list[Tool]:
    return [CLASSIFICATION_TESTS_REFERENCE, STATE_CLASSIFICATION_LAW_LOOKUP]
