# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tests for core.state_portals data integrity.

This is hand-curated data — these tests guard against schema drift,
empty entries, and malformed URLs slipping in when contributors update
the table.
"""
from __future__ import annotations

import pytest

from core.state_portals import FEDERAL_PORTALS, STATE_PORTALS, get_state


REQUIRED_STATE_FIELDS = {
    "name",
    "sos_business_filings_url",
    "business_name_search_url",
    "articles_of_organization_url",
    "annual_report_url",
    "registered_agent_info_url",
    "filing_fee_articles",
    "annual_fee_approximate",
    "notes",
}


def test_has_50_states_plus_dc():
    assert len(STATE_PORTALS) == 51


def test_every_state_has_required_fields():
    for code, data in STATE_PORTALS.items():
        missing = REQUIRED_STATE_FIELDS - set(data.keys())
        assert not missing, f"{code} is missing fields: {missing}"


def test_every_state_has_a_human_readable_name():
    for code, data in STATE_PORTALS.items():
        assert data["name"], f"{code} has no name"
        assert isinstance(data["name"], str)


@pytest.mark.parametrize(
    "url_field",
    [
        "sos_business_filings_url",
        "business_name_search_url",
        "articles_of_organization_url",
        "annual_report_url",
        "registered_agent_info_url",
    ],
)
def test_urls_are_https_when_present(url_field):
    for code, data in STATE_PORTALS.items():
        url = data.get(url_field)
        if url is None:
            continue
        assert url.startswith("https://"), f"{code}.{url_field} is not https: {url!r}"


def test_get_state_accepts_two_letter_code():
    assert get_state("CA")["name"] == "California"
    assert get_state("ca")["name"] == "California"
    assert get_state(" tx ")["name"] == "Texas"


def test_get_state_accepts_full_name():
    assert get_state("Texas")["name"] == "Texas"
    assert get_state("texas")["name"] == "Texas"
    assert get_state("District of Columbia")["name"] == "District of Columbia"


def test_get_state_returns_none_for_unknown():
    assert get_state("XX") is None
    assert get_state("Westeros") is None


def test_get_state_returns_none_for_empty_or_none():
    assert get_state("") is None
    assert get_state(None) is None


def test_full_name_lookup_attaches_code():
    out = get_state("California")
    assert out["_code"] == "CA"


REQUIRED_FEDERAL_KEYS = {
    "ein_application",
    "boi_filing",
    "boi_faq",
    "irs_small_business",
    "uspto_tess",
    "sba_local_assistance",
}


def test_federal_portals_has_required_keys():
    missing = REQUIRED_FEDERAL_KEYS - set(FEDERAL_PORTALS.keys())
    assert not missing, f"FEDERAL_PORTALS missing: {missing}"


def test_all_federal_urls_are_https():
    for key, url in FEDERAL_PORTALS.items():
        assert url.startswith("https://"), f"{key} is not https: {url!r}"
