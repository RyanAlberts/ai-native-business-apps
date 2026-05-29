# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tests for shared helpers."""
from __future__ import annotations

from core.util import normalize_state, slugify, state_code


def test_normalize_state_code_and_name():
    assert normalize_state("tx") == ("TX", "Texas")
    assert normalize_state("TX") == ("TX", "Texas")
    assert normalize_state("texas") == ("TX", "Texas")
    assert normalize_state("Delaware") == ("DE", "Delaware")


def test_normalize_state_unknown_and_empty():
    assert normalize_state("Atlantis") is None
    assert normalize_state("") is None
    assert normalize_state(None) is None


def test_state_code():
    assert state_code("Wyoming") == "WY"
    assert state_code("nope") is None


def test_slugify():
    assert slugify("Acme Bookkeeping, LLC") == "acme-bookkeeping-llc"
    assert slugify("  Multiple   Spaces!! ") == "multiple-spaces"
    assert slugify("") == "untitled"
    assert len(slugify("x" * 200)) <= 60
