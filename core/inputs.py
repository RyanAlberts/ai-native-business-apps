# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Shared run() input handling — the Company spine, threaded into every agent.

The whole thesis of Keel is "fill in your company once." For that to be
real, every standalone agent's ``run()`` has to accept the same shared
``Company`` profile, not just an isolated blob of free text. This module
is the one place that turns whatever a caller hands ``run()`` into the
user message the LLM sees:

    * a ``Company``            → its ``to_context()`` profile block
    * a ``dict``               → coerced to a ``Company``, then profiled
    * a path to ``company.json`` → loaded, then profiled
    * a raw JSON object string → parsed to a ``Company``, then profiled
    * plain free text          → passed through untouched

When a profile is present it's prepended to the message so the agent
reuses known facts instead of re-asking for them. Agents that like to
frame the ask ("Classify this role:\\n\\n…") pass a ``template``; the
founder's text (or, for a Company, any free-text notes) fills ``{input}``.

This keeps the wiring DRY: one helper, one behavior, every agent — and it
stays offline-testable since it never touches the network.
"""
from __future__ import annotations

import json
from pathlib import Path

from .company import Company

__all__ = ["coerce_company", "build_user_message"]


def coerce_company(user_input: object) -> Company | None:
    """Return a ``Company`` if ``user_input`` represents one, else ``None``.

    Recognizes a ``Company``, a ``dict``, a path to an existing
    ``company.json``, or a raw JSON object string. Plain free text returns
    ``None`` (the caller should treat it as the founder's literal message)
    — that's the difference from the Founding Journey's coercion, which
    deliberately wraps free text into a one-line ``Company``.
    """
    if isinstance(user_input, Company):
        return user_input
    if isinstance(user_input, dict):
        return Company.from_dict(user_input)
    if isinstance(user_input, (str, bytes)):
        text = user_input.decode() if isinstance(user_input, bytes) else user_input
        stripped = text.strip()
        if not stripped:
            return None
        # A path to an existing company.json?
        try:
            p = Path(stripped)
            if p.suffix == ".json" and p.exists():
                return Company.load(p)
        except OSError:
            pass
        # A raw JSON object? (Only objects — a bare string/number isn't a profile.)
        if stripped.startswith("{"):
            try:
                return Company.from_dict(json.loads(stripped))
            except json.JSONDecodeError:
                pass
    return None


def build_user_message(user_input: object, *, template: str = "{input}") -> str:
    """Normalize raw ``run()`` input into the user message for the LLM.

    Args:
        user_input: a ``Company``, a ``dict``, a ``company.json`` path, a
            raw JSON object string, or plain free text.
        template: how to frame the founder's text. Must contain ``{input}``.
            Defaults to passing the text through unchanged.

    Returns:
        The user message — the company profile block (when one is present)
        followed by the templated free text.
    """
    company = coerce_company(user_input)
    if company is not None:
        prefix = company.to_context()
        # A structured profile carries no separate "ask"; reuse any free-text
        # notes / one-liner so a templated agent still has something to frame.
        body = (company.notes or company.one_liner or "").strip()
        framed = template.format(input=body) if body else ""
        return "\n\n".join(part for part in (prefix.strip(), framed.strip()) if part)

    text = user_input.decode() if isinstance(user_input, bytes) else str(user_input)
    return template.format(input=text)
