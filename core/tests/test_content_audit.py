# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Regression guard: stale federal-legal claims must not reappear.

Two layers:
  1. Unit tests pin the scanner's behavior — it must catch the stale
     phrasings and must NOT flag the corrected (negated) phrasings.
  2. A repo-wide test scans every agent's source + current baseline so a
     future edit or drifting re-baseline that reintroduces the bad advice
     fails CI instead of shipping to founders.
"""
from __future__ import annotations

from pathlib import Path

from core.content_audit import audit_paths, scan_text

_REPO = Path(__file__).resolve().parents[2]
_ROOTS = [_REPO / "starter_business_agents", _REPO / "advanced_business_agents"]


# ── scanner unit tests: stale phrasings ARE caught ─────────────────────


def test_catches_boi_filing_required():
    bad = "File a BOI report with FinCEN within 90 days of formation."
    rules = {f.rule for f in scan_text(bad)}
    assert "boi_filing_required" in rules


def test_catches_boi_500_per_day_penalty():
    bad = "BOI is high-stakes ($500/day penalties) — always mention it."
    rules = {f.rule for f in scan_text(bad)}
    assert "boi_filing_required" in rules


def test_catches_attach_to_1040():
    bad = "Attach a copy of the signed election letter to your Form 1040."
    rules = {f.rule for f in scan_text(bad)}
    assert "attach_83b_to_1040" in rules


def test_catches_invented_stats():
    bad = "Roughly 40% of small businesses get a finding (avg $845 penalty)."
    rules = {f.rule for f in scan_text(bad)}
    assert "invented_audit_stat" in rules
    assert "invented_penalty_stat" in rules


# ── scanner unit tests: corrected phrasings are NOT flagged ────────────


def test_allows_boi_exemption_phrasing():
    good = (
        "Under FinCEN's 2025 interim final rule, US-formed entities are "
        "exempt from the BOI report; no filing is required. Verify on the "
        "FinCEN FAQ."
    )
    assert scan_text(good) == []


def test_allows_bank_cdd_beneficial_ownership():
    good = (
        "When you open the account, the bank is required under FinCEN's "
        "Customer Due Diligence rule to collect beneficial ownership info."
    )
    assert scan_text(good) == []


def test_allows_corrected_1040_phrasing():
    good = (
        "Since TD 9779 (2016) you do NOT attach the election to your Form "
        "1040 — keep the certified-mail receipt as proof instead."
    )
    assert scan_text(good) == []


def test_json_schema_required_key_not_flagged():
    # `"required": [...]` in a tool input_schema must not trip the BOI rule.
    schema = 'input_schema = {"type": "object", "required": ["state"]}  # boi lookup'
    assert scan_text(schema) == []


def test_loan_doc_1040_list_not_flagged():
    # A loan agent listing "Owner's 1040s" as a required doc is unrelated to
    # the 83(b) election and must not trip the attach-to-1040 rule.
    good = "- Personal tax returns — 2–3 years — Owner's 1040s, all schedules."
    assert scan_text(good) == []


def test_stale_bullet_still_caught_without_negation():
    bad = (
        "- Missing the BOI deadline: you must file a BOI report with FinCEN "
        "within 90 days of formation or face $500/day penalties."
    )
    assert "boi_filing_required" in {f.rule for f in scan_text(bad)}


# ── repo-wide guard ────────────────────────────────────────────────────


def test_no_stale_legal_content_in_repo():
    findings = audit_paths(_ROOTS)
    if findings:
        lines = [
            f"  {f.path.relative_to(_REPO)} [{f.rule}]: {f.excerpt}" for f in findings
        ]
        raise AssertionError(
            "Stale federal-legal content found (see core/content_audit.py):\n"
            + "\n".join(lines)
        )
