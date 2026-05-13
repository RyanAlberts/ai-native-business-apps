# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tools for the Compliance & Tax Setup Agent.

  * `state_compliance_lookup` — given a list of US states the founder
    operates in, return per-state annual-report / franchise-tax URLs, the
    approximate annual fee, the registered-agent reference page, and any
    state-specific notes — plus the federal portal set (IRS, FinCEN BOI,
    SBA). The agent embeds these URLs verbatim in the State Filings and
    Federal Filings sections instead of fabricating them from memory.

Data lives in `core/state_portals.py` (shared across agents). Update there.
"""
from __future__ import annotations

from core import Tool
from core.state_portals import FEDERAL_PORTALS, STATE_PORTALS, get_state


def _state_compliance_lookup(args: dict) -> dict:
    states_input = args.get("states") or []
    if isinstance(states_input, str):
        states_input = [states_input]

    results: list[dict] = []
    unknown: list[str] = []
    for raw in states_input:
        portal = get_state(raw)
        if not portal:
            unknown.append(raw)
            continue
        results.append(
            {
                "state": portal["name"],
                "annual_report_or_franchise_tax_url": portal.get("annual_report_url"),
                "annual_fee_approximate": portal.get("annual_fee_approximate"),
                "sos_business_filings_url": portal.get("sos_business_filings_url"),
                "registered_agent_info_url": portal.get("registered_agent_info_url"),
                "notes": portal.get("notes"),
            }
        )

    return {
        "ok": True,
        "states": results,
        "unknown_inputs": unknown,
        "supported_codes": sorted(STATE_PORTALS.keys()) if unknown else None,
        "federal": {
            "ein_application": FEDERAL_PORTALS.get("ein_application"),
            "boi_filing": FEDERAL_PORTALS.get("boi_filing"),
            "boi_faq": FEDERAL_PORTALS.get("boi_faq"),
            "irs_small_business": FEDERAL_PORTALS.get("irs_small_business"),
            "sba_local_assistance": FEDERAL_PORTALS.get("sba_local_assistance"),
        },
    }


STATE_COMPLIANCE_LOOKUP = Tool(
    name="state_compliance_lookup",
    description=(
        "Return state-specific compliance + annual-filing references for one "
        "or more US states the founder operates in. For each state, returns "
        "the annual-report / franchise-tax page, approximate annual fee, "
        "Secretary of State business-filings page, registered-agent reference, "
        "and state-specific notes (tax quirks, publication requirements, "
        "etc.). Also returns federal portal URLs (IRS EIN, FinCEN BOI, IRS "
        "business taxes, SBA). Call this ONCE with the full list of states "
        "the founder operates in. Embed the returned URLs directly in the "
        "State Filings and Federal Filings sections — do not invent URLs."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "states": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "US states the founder operates in. Accept 2-letter codes "
                    "(e.g. 'TX') or full names (e.g. 'Texas'). Include the "
                    "state of formation AND every state of operation."
                ),
            },
        },
        "required": ["states"],
    },
    handler=_state_compliance_lookup,
)


def all_tools() -> list[Tool]:
    return [STATE_COMPLIANCE_LOOKUP]
