# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Small shared helpers used across agents.

Previously each agent re-implemented its own `_normalize_state()` and a
slug helper. They now live here so there's one canonical implementation
(and one place to fix a bug).
"""
from __future__ import annotations

import re

from .state_portals import STATE_PORTALS


def normalize_state(state: str | None) -> tuple[str, str] | None:
    """Resolve a free-text US state to its ``(code, name)``.

    Accepts a 2-letter code or a full name, case-insensitively:
    ``"tx"``, ``"TX"``, ``"Texas"``, ``"texas"`` all return
    ``("TX", "Texas")``.

    Returns ``None`` if the input matches no known state — callers should
    surface a helpful error rather than guessing.
    """
    if not state:
        return None
    key = state.strip().upper()
    if key in STATE_PORTALS:
        return key, STATE_PORTALS[key]["name"]  # type: ignore[return-value]
    lower = state.strip().lower()
    for code, data in STATE_PORTALS.items():
        if (data.get("name") or "").lower() == lower:
            return code, data["name"]  # type: ignore[return-value]
    return None


def state_code(state: str | None) -> str | None:
    """Return just the 2-letter code for a state, or ``None``."""
    resolved = normalize_state(state)
    return resolved[0] if resolved else None


def slugify(text: str, *, maxlen: int = 60) -> str:
    """Lowercase, hyphenate, strip to a filesystem/URL-safe slug.

    ``"Acme Bookkeeping, LLC"`` -> ``"acme-bookkeeping-llc"``.
    """
    slug = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return slug[:maxlen].strip("-") or "untitled"
