# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tests for the prepare-to-submit artifact layer."""
from __future__ import annotations

from core.artifacts import (
    ArtifactSet,
    html_artifact,
    ics_artifact,
    letter_html,
    markdown_artifact,
)


def test_artifactset_write_creates_files(tmp_path):
    s = ArtifactSet()
    s.add(markdown_artifact("plan.md", "# Plan", label="Plan"))
    s.add(markdown_artifact("notes.md", "notes"))
    paths = s.write(tmp_path)
    assert len(paths) == 2
    assert (tmp_path / "plan.md").read_text() == "# Plan"
    assert len(s) == 2


def test_manifest_shape():
    s = ArtifactSet().add(markdown_artifact("a.md", "x", label="A"))
    m = s.manifest()
    assert m == [{"filename": "a.md", "mimetype": "text/markdown", "label": "A"}]


def test_html_artifact_is_self_contained():
    art = html_artifact("doc.html", title="Title", body_html="<h1>Hi</h1>")
    assert art.content.startswith("<!doctype html>")
    assert "<h1>Hi</h1>" in art.content
    assert art.mimetype == "text/html"


def test_letter_html_escapes_and_paragraphs():
    art = letter_html("l.html", title="Letter", body_text="a <b>\n\npara two")
    assert "&lt;b&gt;" in art.content  # escaped
    assert art.content.count("<p>") == 2


def test_ics_emits_valid_vevents():
    art = ics_artifact(
        "deadlines.ics",
        [
            {"date": "2026-04-15", "summary": "DE Franchise Tax", "description": "Pay APVC"},
            {"date": "bad-date", "summary": "Skipped"},
        ],
    )
    body = art.content
    assert body.startswith("BEGIN:VCALENDAR")
    assert body.count("BEGIN:VEVENT") == 1  # malformed date skipped
    assert "DTSTART;VALUE=DATE:20260415" in body
    assert "SUMMARY:DE Franchise Tax" in body
    assert art.content.endswith("\r\n")


def test_ics_escapes_special_chars():
    art = ics_artifact("d.ics", [{"date": "2026-01-01", "summary": "A; B, C"}])
    assert "SUMMARY:A\\; B\\, C" in art.content


def test_ics_neutralizes_crlf_injection():
    # A stray CR/LF in attacker- or LLM-supplied text must not break out of
    # the content line and inject a new property or VEVENT (RFC 5545 §3.1).
    art = ics_artifact(
        "d.ics",
        [{"date": "2026-01-01", "summary": "Evil\r\nBEGIN:VEVENT\r\nUID:injected"}],
    )
    lines = art.content.split("\r\n")
    # Exactly one real VEVENT line and one real UID line — the injected ones
    # survive only as escaped text inside the SUMMARY value.
    assert sum(1 for ln in lines if ln == "BEGIN:VEVENT") == 1
    assert sum(1 for ln in lines if ln.startswith("UID:")) == 1
    # No raw CR may appear except as part of a CRLF line ending.
    assert art.content.count("\r") == art.content.count("\r\n")
    assert "SUMMARY:Evil\\nBEGIN:VEVENT\\nUID:injected" in art.content
