# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tools for the Founding Journey.

The journey reuses each specialist agent's own tools (imported in
`journey.py`), so the synthesis step itself needs none. This stub keeps
the agent folder structurally consistent with the rest of the repo.
"""
from __future__ import annotations

from core import Tool


def all_tools() -> list[Tool]:
    return []
