# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Founding Journey — the unified Day-0 back-office orchestrator.

Runs the core formation agents (incorporation → 83(b) → legal docs →
banking & insurance → compliance & tax) as one threaded pipeline over a
shared ``Company`` profile, then synthesizes a single Day-0 Formation
Packet with prepare-to-submit artifacts.
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

from core import Company

from .journey import JourneyResult, run_journey

__all__ = ["run", "JourneyResult", "run_journey"]


def _coerce_company(user_input) -> Company:
    """Accept a Company, a dict, a company.json path, JSON text, or a brief."""
    if isinstance(user_input, Company):
        return user_input
    if isinstance(user_input, dict):
        return Company.from_dict(user_input)
    if isinstance(user_input, (str, bytes)):
        text = user_input.decode() if isinstance(user_input, bytes) else user_input
        stripped = text.strip()
        # A path to an existing company.json?
        try:
            p = Path(stripped)
            if p.suffix == ".json" and p.exists():
                return Company.load(p)
        except OSError:
            pass
        # Raw JSON object?
        if stripped.startswith("{"):
            try:
                return Company.from_dict(json.loads(stripped))
            except json.JSONDecodeError:
                pass
        # Otherwise: free-text brief.
        return Company(one_liner=stripped, notes=stripped)
    raise TypeError(f"Cannot build a Company from {type(user_input).__name__}")


async def run(user_input, on_step=None) -> JourneyResult:
    """Run the founding journey.

    Args:
        user_input: a ``Company``, a dict, a path to ``company.json``, raw
            JSON, or a free-text business description.
        on_step: optional callback fired after each step (for UI progress).

    Returns:
        A ``JourneyResult`` (``.final`` is the synthesized packet;
        ``.artifacts()`` returns the downloadable deliverables).
    """
    company = _coerce_company(user_input)
    return await run_journey(company, on_step=on_step)


if __name__ == "__main__":
    import sys

    default = Company(
        legal_name="Northwind Robotics, Inc.",
        one_liner="Warehouse picking robots sold to mid-size 3PLs",
        industry="Robotics / hardware",
        home_state="California",
        state_of_formation="Delaware",
        entity_type="C-Corp",
        funding_stage="Priced seed (9–18 months)",
        employees_plan="1–5 employees",
        liability_notes="Hardware in customer warehouses; product-liability exposure.",
    )
    arg = " ".join(sys.argv[1:]).strip()
    result = asyncio.run(run(arg or default))
    print(result.final)
