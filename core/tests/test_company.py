# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tests for the shared Company profile."""
from __future__ import annotations

from core.company import Company, Founder


def test_roundtrip_json_preserves_founders():
    c = Company(
        legal_name="Acme Bookkeeping, LLC",
        home_state="Texas",
        one_liner="SaaS for plumbers",
        founders=[Founder(name="Ada", role="CEO", equity_pct=60.0)],
    )
    restored = Company.from_json(c.to_json())
    assert restored.legal_name == "Acme Bookkeeping, LLC"
    assert restored.founders[0].name == "Ada"
    assert restored.founders[0].equity_pct == 60.0


def test_from_dict_ignores_unknown_keys():
    c = Company.from_dict({"legal_name": "X", "bogus_field": 123})
    assert c.legal_name == "X"


def test_to_brief_omits_empty_fields():
    brief = Company(legal_name="X", home_state="WY").to_brief()
    assert "Business: X" in brief
    assert "Founder home state: Wyoming" not in brief  # not normalized in brief
    assert "EIN" not in brief  # empty -> omitted


def test_to_context_blank_when_empty():
    assert Company().to_context() == ""
    assert "Known company profile" in Company(legal_name="X").to_context()


def test_formation_state_code_falls_back_to_home_state():
    assert Company(home_state="texas").formation_state_code == "TX"
    assert Company(state_of_formation="Delaware").formation_state_code == "DE"
    assert Company().formation_state_code is None


def test_missing_for_formation():
    assert set(Company().missing_for_formation()) == {
        "legal_name",
        "home_state",
        "one_liner",
    }
    ready = Company(legal_name="X", home_state="WY", one_liner="y")
    assert ready.missing_for_formation() == []


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "company.json"
    Company(legal_name="Saved Co").save(path)
    assert path.exists()
    assert Company.load(path).legal_name == "Saved Co"


def test_load_missing_file_returns_empty(tmp_path):
    assert Company.load(tmp_path / "nope.json") == Company()
