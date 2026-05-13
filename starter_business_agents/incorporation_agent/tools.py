# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tools for the Incorporation Agent.

Two tools, both deterministic / no network calls:

  * `state_business_name_search` — given a state and a proposed business name,
    return the canonical SoS name-search URL plus instructions. The agent
    surfaces this in the Filing Checklist so the founder runs the lookup
    themselves (state databases vary wildly; scraping them is unreliable).

  * `state_portal_lookup` — return the full bundle of portal links + fee
    estimates + state-specific notes for the recommended state. The agent
    embeds these URLs directly in the output.

Data lives in `core/state_portals.py` (shared across agents). Update there, not here.
"""
from __future__ import annotations

from core import Tool
from core.state_portals import FEDERAL_PORTALS, STATE_PORTALS, get_state


def _state_business_name_search(args: dict) -> dict:
    """Return the SoS name-search URL + instructions for a state + name."""
    state_input = args.get("state", "")
    business_name = args.get("business_name", "")
    portal = get_state(state_input)
    if not portal:
        return {
            "ok": False,
            "error": f"Unknown state: {state_input!r}. Use a 2-letter code or full state name.",
            "supported_codes": sorted(STATE_PORTALS.keys()),
        }
    return {
        "ok": True,
        "state": portal["name"],
        "business_name_queried": business_name,
        "business_name_search_url": portal.get("business_name_search_url"),
        "sos_business_filings_url": portal.get("sos_business_filings_url"),
        "instructions": (
            f"1. Open the URL above in a browser.\n"
            f"2. Search for the EXACT proposed name: '{business_name}'.\n"
            f"3. Then search for the root word(s) of the name alone (e.g. for "
            f"'Acme Books LLC', also try 'Acme Books' and 'Acme').\n"
            f"4. Review results for: (a) exact matches, (b) confusingly similar "
            f"names sharing the same root, (c) names with only minor variations "
            f"(plural/singular, 'Co.' vs 'Inc.', different entity suffixes).\n"
            f"5. If anything looks similar, the SoS may reject your filing on "
            f"'deceptively similar' grounds — either pick a more distinctive "
            f"name or consult an attorney about whether your name is "
            f"distinguishable enough.\n"
            f"6. Optional federal check: search USPTO TESS "
            f"({FEDERAL_PORTALS['uspto_tess']}) for trademark conflicts."
        ),
        "what_to_look_for": [
            "Exact match of your proposed name",
            "Same root word with different entity suffix (LLC vs Inc. vs Corp)",
            "Plural/singular variations",
            "Common typos or transpositions",
            "Names that would mislead a customer searching for yours",
        ],
        "state_notes": portal.get("notes"),
    }


STATE_BUSINESS_NAME_SEARCH = Tool(
    name="state_business_name_search",
    description=(
        "Return the official Secretary of State business-name-search URL for a "
        "given US state, plus instructions on how to verify a proposed name is "
        "available. Use this whenever the founder mentions a specific business "
        "name. The founder runs the actual lookup in their browser — this tool "
        "does not scrape state databases."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "state": {
                "type": "string",
                "description": "US state — either 2-letter code (e.g. 'TX') or full name (e.g. 'Texas').",
            },
            "business_name": {
                "type": "string",
                "description": "The exact proposed business name the founder wants to verify.",
            },
        },
        "required": ["state", "business_name"],
    },
    handler=_state_business_name_search,
)


def _state_portal_lookup(args: dict) -> dict:
    """Return the full portal bundle for a state + the federal portal set."""
    state_input = args.get("state", "")
    portal = get_state(state_input)
    if not portal:
        return {
            "ok": False,
            "error": f"Unknown state: {state_input!r}. Use a 2-letter code or full state name.",
            "supported_codes": sorted(STATE_PORTALS.keys()),
        }
    return {
        "ok": True,
        "state": portal,
        "federal": FEDERAL_PORTALS,
    }


STATE_PORTAL_LOOKUP = Tool(
    name="state_portal_lookup",
    description=(
        "Return the full bundle of state-specific incorporation portal links "
        "(Secretary of State main page, business-name search, articles of "
        "organization form, annual report, registered agent info) plus filing "
        "fee estimates and state-specific notes. ALSO returns the federal "
        "portal set (IRS EIN application, FinCEN BOI filing, USPTO trademark "
        "search, SBA resources). Call this for the recommended state of "
        "formation and embed the URLs directly in the Filing Checklist and "
        "Key Documents sections of the output."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "state": {
                "type": "string",
                "description": "US state — either 2-letter code (e.g. 'TX') or full name (e.g. 'Texas').",
            },
        },
        "required": ["state"],
    },
    handler=_state_portal_lookup,
)


def all_tools() -> list[Tool]:
    return [STATE_BUSINESS_NAME_SEARCH, STATE_PORTAL_LOOKUP]
