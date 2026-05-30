# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tests for shared run() input handling — the Company spine wiring.

These verify the one behavior every agent now relies on: free text passes
through (optionally framed by a template), while a Company / dict / JSON /
company.json path is recognized and rendered into the profile block agents
prepend so they don't re-ask for known facts.
"""
from __future__ import annotations

import json

from core import Company, build_user_message, coerce_company, merge_company


def test_plain_text_passes_through():
    assert build_user_message("just some text") == "just some text"


def test_plain_text_is_templated():
    out = build_user_message("a role", template="Classify this role:\n\n{input}")
    assert out == "Classify this role:\n\na role"


def test_coerce_company_returns_none_for_free_text():
    assert coerce_company("two founders in Texas") is None


def test_company_profile_is_prepended():
    c = Company(legal_name="Northwind Robotics, Inc.", home_state="California")
    out = build_user_message(c)
    assert "Known company profile" in out
    assert "Northwind Robotics" in out


def test_company_notes_render_in_profile_block():
    # A Company renders its full profile (notes included); the template is
    # not applied to a structured profile, so notes appear once, not twice.
    c = Company(legal_name="Acme, LLC", notes="Need a mutual NDA")
    out = build_user_message(c, template="Request:\n\n{input}")
    assert "Known company profile" in out
    assert "Need a mutual NDA" in out
    assert out.count("Need a mutual NDA") == 1
    assert "Request:" not in out  # template is for free text only


def test_dict_is_coerced_to_company():
    out = build_user_message({"legal_name": "Acme, LLC", "home_state": "Texas"})
    assert "Known company profile" in out
    assert "Acme, LLC" in out


def test_raw_json_object_is_coerced():
    blob = json.dumps({"legal_name": "JSON Co", "industry": "SaaS"})
    out = build_user_message(blob)
    assert "Known company profile" in out
    assert "JSON Co" in out


def test_company_json_path_is_loaded(tmp_path):
    c = Company(legal_name="Saved Co", home_state="Delaware")
    path = tmp_path / "company.json"
    path.write_text(c.to_json(), encoding="utf-8")
    out = build_user_message(str(path))
    assert "Saved Co" in out


def test_empty_company_yields_empty_message():
    # No known facts and no notes → nothing to prepend or frame.
    assert build_user_message(Company()) == ""


# ── merge_company (the UI form → agent bridge) ─────────────────────────


def test_merge_onto_none_starts_fresh():
    c = merge_company(None, legal_name="Acme, LLC", funding_stage="Bootstrap")
    assert c.legal_name == "Acme, LLC"
    assert c.funding_stage == "Bootstrap"


def test_merge_blank_does_not_clobber_loaded_value():
    base = Company(legal_name="Loaded Co", home_state="California")
    merged = merge_company(base, legal_name="", home_state="Texas")
    # Blank legal_name is ignored; non-empty home_state overrides.
    assert merged.legal_name == "Loaded Co"
    assert merged.home_state == "Texas"


def test_merge_appends_notes_without_replacing():
    base = Company(legal_name="Acme", notes="Existing note.")
    merged = merge_company(base, notes="New ask.")
    assert "Existing note." in merged.notes
    assert "New ask." in merged.notes


def test_merge_does_not_mutate_base():
    base = Company(legal_name="Acme")
    merge_company(base, funding_stage="Seed", notes="x")
    # Original is untouched (replace returns a new instance).
    assert base.funding_stage == ""
    assert base.notes == ""
