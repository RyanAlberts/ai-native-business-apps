# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tests for the shared legal-disclaimer layer.

The disclaimer is appended at every export boundary (markdown download,
CLI stdout, Founding Journey artifacts), so the two properties that
actually matter are: it shows up once, and it never stacks.
"""
from __future__ import annotations

from core import DISCLAIMER, with_disclaimer
from core.brand import _DISCLAIMER_MARKER, disclaimer_md


def test_with_disclaimer_appends_footer():
    out = with_disclaimer("# Plan\n\nbody")
    assert out.startswith("# Plan")
    assert DISCLAIMER in out
    assert _DISCLAIMER_MARKER in out


def test_with_disclaimer_is_idempotent():
    once = with_disclaimer("some output")
    twice = with_disclaimer(once)
    # Applying it again must not stack a second footer.
    assert once == twice
    assert twice.count(_DISCLAIMER_MARKER) == 1
    assert twice.count(DISCLAIMER) == 1


def test_with_disclaimer_noop_on_empty():
    assert with_disclaimer("") == ""
    assert with_disclaimer(None) is None  # type: ignore[arg-type]


def test_disclaimer_md_carries_marker():
    assert _DISCLAIMER_MARKER in disclaimer_md()
    assert DISCLAIMER in disclaimer_md()
