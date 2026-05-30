# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Stale-legal-content guard.

The 2026-05 correctness pass fixed three places where agents asserted
out-of-date federal rules (BOI/CTA, the DOL 2024 contractor rule, 83(b)
Form-1040 attachment). This module makes those fixes *stick*: it scans
agent source (prompts/tools/apps) and the current baselines for the stale
claims so a future edit — or a re-baseline that drifts — fails CI instead
of silently shipping wrong advice to founders.

The hard part is precision. The corrected text still *mentions* these
topics, just in negated form ("US-formed entities are **exempt** from
BOI", "you do **not** attach the election to your Form 1040"), and the
bank's Customer Due Diligence beneficial-ownership form is legitimately
"required". So each rule is paragraph-scoped: a paragraph trips a rule
only when a stale trigger is present AND none of that rule's allow-phrases
(the markers of correct, current framing) appear in the same paragraph.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Rule:
    name: str
    why: str
    # All trigger patterns must match the paragraph for the rule to fire…
    triggers: tuple[str, ...]
    # …unless any allow pattern also matches (the corrected/legit framing).
    allow: tuple[str, ...] = ()


# Patterns are matched case-insensitively against each paragraph.
RULES: tuple[Rule, ...] = (
    Rule(
        name="invented_audit_stat",
        why="Unsourced '40% of small businesses' misclassification statistic.",
        triggers=(r"40\s*%\s*of\s+(?:us\s+)?small\s+business",),
    ),
    Rule(
        name="invented_penalty_stat",
        why="Unsourced '$845 average penalty' statistic.",
        triggers=(r"\$845\b",),
    ),
    Rule(
        name="boi_filing_required",
        why=(
            "Tells a US-formed entity to file a FinCEN BOI report / quotes a "
            "BOI deadline or penalty. US-formed entities are exempt under the "
            "2025 interim final rule."
        ),
        triggers=(
            r"\bboi\b|beneficial ownership information",
            # Advice-shaped phrasing only — NOT a bare "required" (which also
            # appears in JSON-schema `"required": [...]` keys and in correct
            # negated guidance like "no BOI filing is required").
            r"must file|file a boi|required to file|required for (?:most|all|your|llc|every)"
            r"|within 90 days|90 days of formation|\$?500\s*/\s*day|500 per day|penalt",
        ),
        allow=(
            # Markers of the correct, current framing or a legitimate use.
            r"exempt|not required|no longer|do not need|don't need|isn't required"
            r"|doesn't|does not (?:need|have)|foreign|customer due diligence|cdd"
            r"|the bank|bank is required|bank's|2025|interim final rule|do not|don't"
            r"|verify|faq|out of date|out-of-date|no boi",
        ),
    ),
    Rule(
        name="attach_83b_to_1040",
        why=(
            "Says to attach the 83(b) election to Form 1040 / the tax return. "
            "TD 9779 (2016) removed that requirement."
        ),
        triggers=(
            # Must be about the 83(b) election specifically — keeps unrelated
            # "attach … Owner's 1040s" loan-doc lists from matching.
            r"83\(b\)|election",
            r"attach",
            r"form 1040|1040|tax return",
        ),
        allow=(
            r"\bnot\b|n't|no longer|removed|td 9779|do not|before you file"
            r"|tell your cpa|verify",
        ),
    ),
)

# Files whose content we audit: agent source + the current baselines. We
# deliberately do NOT scan core/ (this module names the stale strings) or
# historical baselines (see latest_baselines()).
_SOURCE_GLOBS = ("prompts.py", "tools.py", "app.py", "agent.py", "README.md", "WALKTHROUGH.md")


@dataclass(frozen=True)
class Finding:
    path: Path
    rule: str
    why: str
    excerpt: str


def _paragraphs(text: str) -> list[str]:
    # Blank-line-separated blocks. We scope to the paragraph (not the line)
    # so a trigger is judged together with any negation in its own context
    # — corrected guidance keeps the negation in the same block. A bullet
    # list is one block here, which is the right granularity: its items
    # share a heading/lead-in that carries the framing.
    return [p for p in re.split(r"\n\s*\n", text) if p.strip()]


def scan_text(text: str, *, path: Path | None = None) -> list[Finding]:
    """Return findings for one document's text."""
    findings: list[Finding] = []
    for para in _paragraphs(text):
        low = para.lower()
        for rule in RULES:
            if not all(re.search(t, low) for t in rule.triggers):
                continue
            if any(re.search(a, low) for a in rule.allow):
                continue
            findings.append(
                Finding(
                    path=path or Path("<text>"),
                    rule=rule.name,
                    why=rule.why,
                    excerpt=" ".join(para.split())[:200],
                )
            )
    return findings


def latest_baselines(agent_dir: Path) -> list[Path]:
    """The most recent baseline file in an agent's tests/baselines dir.

    Baselines are date-stamped (``claude-YYYY-MM-DD[...].md``). Only the
    newest is the current behavior; older ones are historical pre-correction
    snapshots and are intentionally left untouched, so we don't audit them.
    """
    bdir = agent_dir / "tests" / "baselines"
    if not bdir.is_dir():
        return []
    files = sorted(bdir.glob("claude-*.md"))
    if not files:
        return []

    def _date_key(p: Path) -> str:
        m = re.search(r"(\d{4}-\d{2}-\d{2})", p.name)
        return m.group(1) if m else ""

    newest = max(_date_key(f) for f in files)
    return [f for f in files if _date_key(f) == newest]


def audit_paths(roots: list[Path]) -> list[Finding]:
    """Audit agent source + current baselines under each root directory."""
    findings: list[Finding] = []
    seen: set[Path] = set()
    for root in roots:
        # Agent source files.
        for pattern in _SOURCE_GLOBS:
            for path in root.rglob(pattern):
                if "baselines" in path.parts or "runs" in path.parts:
                    continue
                if path in seen:
                    continue
                seen.add(path)
                findings += scan_text(path.read_text(encoding="utf-8"), path=path)
        # Current baseline per agent (newest only).
        for golden in root.rglob("tests/golden.jsonl"):
            for baseline in latest_baselines(golden.parent.parent):
                if baseline in seen:
                    continue
                seen.add(baseline)
                findings += scan_text(baseline.read_text(encoding="utf-8"), path=baseline)
    return findings
