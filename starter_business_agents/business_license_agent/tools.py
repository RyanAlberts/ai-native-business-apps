# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tools for the Business License + DBA Agent.

Two deterministic tools cover the parts that don't change much:

  * `dba_filing_jurisdiction(state)` — given a US state, return where
    Doing-Business-As (a.k.a. Assumed Name / Fictitious Business Name)
    filings are made: STATE level (Secretary of State), COUNTY level
    (county clerk / recorder), CITY level (city/town clerk), or NONE
    REQUIRED for the founder's entity. Plus the home-state portal URL.

  * `state_general_business_license(state)` — return whether the state
    has a GENERAL state-level business license requirement (most don't —
    only a handful), with the licensing URL when applicable.

The long-tail (specific city/county licensing URLs, industry-specific
permits, zoning restrictions) is handled by the agent via WebSearch.
There are 3,000+ US counties and ~19,000 incorporated municipalities —
hand-curating them all in a static table is out of scope; pointing at
the right one at runtime is exactly what the LLM + web search is good at.

Data is curated from each state's Secretary of State / Department of
Revenue authoritative pages, captured at module-author time. Stale URLs
should be fixed here, and every response always cites the source URL so
the founder can verify.
"""
from __future__ import annotations

from core import Tool
from core.util import state_code as _normalize_state  # shared canonical lookup


# DBA filing jurisdiction by state. Values:
#   "state"       — file Doing-Business-As / Assumed Name / Fictitious Name
#                   with the Secretary of State.
#   "county"      — file with the county clerk / recorder where the business
#                   has its principal place of business.
#   "city"        — file with the city/town clerk (rare; New England states).
#   "state+county"— must file at BOTH state and county levels.
#   "not_required"— state does not require DBA filings for entities (rare).
#
# Source: each state's SoS site + Cornell Legal Information Institute
#   "Fictitious Business Name" surveys, as of module-author time.
_DBA_JURISDICTION: dict[str, dict[str, str]] = {
    "AL": {"level": "state", "url": "https://www.sos.alabama.gov/business-entities", "notes": "File 'Trade Name' registration with AL Secretary of State."},
    "AK": {"level": "state", "url": "https://www.commerce.alaska.gov/web/cbpl/Corporations.aspx", "notes": "File 'Business Name Registration' with the Division of Corporations."},
    "AZ": {"level": "county", "url": "https://azcc.gov/corporations", "notes": "AZ does NOT require a state-level DBA; trade name registration is OPTIONAL with the SoS. Most founders skip it."},
    "AR": {"level": "state", "url": "https://www.sos.arkansas.gov/business-commercial-services-bcs", "notes": "File 'Application for Fictitious Name' with AR SoS."},
    "CA": {"level": "county", "url": "", "notes": "File 'Fictitious Business Name' (FBN) with the county clerk where the business is located. Each CA county runs its own FBN system."},
    "CO": {"level": "state", "url": "https://www.sos.state.co.us/pubs/business/main.html", "notes": "File 'Trade Name Registration' with CO SoS."},
    "CT": {"level": "city", "url": "https://business.ct.gov/", "notes": "File 'Certificate of Trade Name' with each town clerk where the business operates."},
    "DE": {"level": "county", "url": "https://corp.delaware.gov/", "notes": "File 'Registration of Trade, Business & Fictitious Names' with the Prothonotary of the Superior Court in each Delaware county where the business operates."},
    "DC": {"level": "state", "url": "https://dcra.dc.gov/", "notes": "File 'Trade Name Registration' with DCRA (the District's licensing agency)."},
    "FL": {"level": "state", "url": "https://dos.fl.gov/sunbiz/", "notes": "File 'Fictitious Name Registration' with FL Division of Corporations (SunBiz)."},
    "GA": {"level": "county", "url": "", "notes": "File 'Trade Name Registration' with the county Superior Court clerk where the business operates."},
    "HI": {"level": "state", "url": "https://cca.hawaii.gov/breg/", "notes": "File 'Application for Registration of Trade Name' with HI BREG."},
    "ID": {"level": "state", "url": "https://sosbiz.idaho.gov/", "notes": "File 'Certificate of Assumed Business Name' with ID SoS."},
    "IL": {"level": "county", "url": "", "notes": "File 'Assumed Name Certificate' with the county clerk where the business is located. State-level filing for IL corps via SoS."},
    "IN": {"level": "county", "url": "", "notes": "File 'Certificate of Assumed Business Name' with the county recorder. IN SoS also accepts entity-level DBAs."},
    "IA": {"level": "state", "url": "https://sos.iowa.gov/business/", "notes": "File 'Fictitious Name Resolution' with IA SoS for entities."},
    "KS": {"level": "not_required", "url": "https://www.sos.ks.gov/business/business.html", "notes": "Kansas does NOT require DBA registration. Entities operate under their registered name; trade-name use is allowed without filing."},
    "KY": {"level": "state+county", "url": "https://sos.ky.gov/bus/business-filings/", "notes": "File 'Certificate of Assumed Name' with the SoS AND the county clerk where the principal office is located."},
    "LA": {"level": "state", "url": "https://www.sos.la.gov/BusinessServices/", "notes": "File 'Application to Register Trade Name' with LA SoS."},
    "ME": {"level": "state", "url": "https://www.maine.gov/sos/cec/corp/", "notes": "File 'Statement of Intention to do Business under an Assumed Name' with ME SoS."},
    "MD": {"level": "state", "url": "https://egov.maryland.gov/businessexpress", "notes": "File 'Trade Name Application' with MD SDAT via Maryland Business Express."},
    "MA": {"level": "city", "url": "", "notes": "File 'Business Certificate' (DBA) with the city/town clerk where the business is located. Each municipality runs its own."},
    "MI": {"level": "state+county", "url": "https://www.michigan.gov/lara/bureau-list/cscl/corp", "notes": "Entities file 'Certificate of Assumed Name' with LARA; sole proprietors file with county clerk."},
    "MN": {"level": "state", "url": "https://www.sos.state.mn.us/business-liens/", "notes": "File 'Certificate of Assumed Name' with MN SoS. Must also publish in a local newspaper."},
    "MS": {"level": "county", "url": "", "notes": "File 'Application for Registration of Fictitious Name' with the chancery clerk in each county where the business operates."},
    "MO": {"level": "state", "url": "https://www.sos.mo.gov/business/corporations/", "notes": "File 'Registration of Fictitious Name' with MO SoS."},
    "MT": {"level": "state", "url": "https://sosmt.gov/business/", "notes": "File 'Assumed Business Name' with MT SoS via ePass Montana."},
    "NE": {"level": "state", "url": "https://sos.nebraska.gov/business-services", "notes": "File 'Trade Name Registration' with NE SoS. Renewal every 10 years."},
    "NV": {"level": "county", "url": "", "notes": "File 'Fictitious Firm Name' (DBA) with the county clerk where the business is located."},
    "NH": {"level": "state", "url": "https://www.sos.nh.gov/corporate-division", "notes": "File 'Trade Name Registration' with NH SoS Corporation Division."},
    "NJ": {"level": "state+county", "url": "https://www.nj.gov/treasury/revenue/", "notes": "Corporations/LLCs file 'Alternate Name Registration' with NJ DoR; sole proprietors / partnerships file with the county clerk."},
    "NM": {"level": "state", "url": "https://www.sos.state.nm.us/business-services/", "notes": "NM does not require DBA for sole proprietors; entities may file 'Application for Use of Trade Name' with SoS."},
    "NY": {"level": "state+county", "url": "https://dos.ny.gov/corporations-state-records-and-uniform-commercial-code", "notes": "Corporations file 'Certificate of Assumed Name' with DoS. Sole proprietors / partnerships file 'Business Certificate' (DBA) with the county clerk."},
    "NC": {"level": "county", "url": "", "notes": "File 'Assumed Business Name Certificate' with the county Register of Deeds where the business is located."},
    "ND": {"level": "state", "url": "https://firststop.sos.nd.gov/", "notes": "File 'Trade Name Registration' with ND SoS via FirstStop."},
    "OH": {"level": "state", "url": "https://www.ohiosos.gov/businesses/", "notes": "File 'Trade Name / Fictitious Name Registration' with OH SoS."},
    "OK": {"level": "state", "url": "https://www.sos.ok.gov/business/", "notes": "File 'Trade Name Report' with OK SoS."},
    "OR": {"level": "state", "url": "https://sos.oregon.gov/business/", "notes": "File 'Assumed Business Name Registration' with OR SoS."},
    "PA": {"level": "state", "url": "https://www.dos.pa.gov/BusinessCharities/Business/", "notes": "File 'Fictitious Name Registration' with PA Department of State."},
    "RI": {"level": "city", "url": "", "notes": "File 'Doing Business As Certificate' with the city/town clerk where the business is located."},
    "SC": {"level": "county", "url": "", "notes": "SC does not require state-level DBA. Some counties require fictitious name registration with the Register of Deeds; many do not."},
    "SD": {"level": "state", "url": "https://sosenterprise.sd.gov/BusinessServices/", "notes": "File 'Fictitious Name Statement' with SD SoS."},
    "TN": {"level": "state", "url": "https://sos.tn.gov/business-services", "notes": "File 'Application for Registration of Assumed Corporate Name' with TN SoS for entities; sole proprietors file with county register of deeds."},
    "TX": {"level": "state+county", "url": "https://www.sos.state.tx.us/corp/", "notes": "Entities file 'Assumed Name Certificate' with TX SoS AND the county clerk in every county where the business operates."},
    "UT": {"level": "state", "url": "https://corporations.utah.gov/", "notes": "File 'Registration of Assumed Name' with UT Division of Corporations."},
    "VT": {"level": "state", "url": "https://sos.vermont.gov/corporations/", "notes": "File 'Assumed Business Name Registration' with VT SoS Corporations Division."},
    "VA": {"level": "state+county", "url": "https://www.scc.virginia.gov/pages/Welcome-Business-Entity-Search-Filing", "notes": "Entities file 'Assumed/Fictitious Name Certificate' with the State Corporation Commission AND the circuit court clerk in each city/county of operation."},
    "WA": {"level": "state", "url": "https://dor.wa.gov/open-business/business-licensing", "notes": "WA combines DBA + business license through the Business Licensing Service. File 'Trade Name Registration' there."},
    "WV": {"level": "state", "url": "https://sos.wv.gov/business-licensing/", "notes": "File 'Application for Reservation of Business Name' / 'Trade Name' with WV SoS."},
    "WI": {"level": "state", "url": "https://www.wdfi.org/corporations/", "notes": "WI does NOT have a separate state DBA filing for entities; entities may operate under any assumed name. Sole proprietors register with the county Register of Deeds."},
    "WY": {"level": "state", "url": "https://sos.wyo.gov/Business/", "notes": "File 'Trade Name Registration' with WY SoS."},
}


# Whether the state imposes a GENERAL state-level business license
# requirement (most do NOT — only a handful). This is distinct from
# state-level industry-specific licenses (e.g. cosmetology, food
# handling, contractors) which exist almost everywhere.
_STATE_GENERAL_LICENSE: dict[str, dict[str, str | bool]] = {
    "AK": {"required": True, "name": "Alaska Business License", "url": "https://www.commerce.alaska.gov/web/cbpl/businesslicensing.aspx", "fee_approx": "$50/year"},
    "DE": {"required": True, "name": "Delaware Business License", "url": "https://onestop.delaware.gov/", "fee_approx": "$75/year minimum"},
    "HI": {"required": True, "name": "Hawaii General Excise Tax (GET) License", "url": "https://tax.hawaii.gov/geninfo/get/", "fee_approx": "$20 one-time"},
    "NV": {"required": True, "name": "Nevada State Business License", "url": "https://www.nvsos.gov/sos/businesses/silver-flume-business-portal", "fee_approx": "$200/year for Corps/LLCs"},
    "WA": {"required": True, "name": "Washington Business License", "url": "https://dor.wa.gov/open-business/business-licensing", "fee_approx": "$90 application + endorsements vary"},
}


def _dba_filing_jurisdiction(args: dict) -> dict:
    state_raw = args.get("state") or ""
    state = _normalize_state(state_raw)
    if state is None:
        return {
            "ok": False,
            "error": f"unknown state: {state_raw!r}. Use a 2-letter code or full name.",
            "supported_codes": sorted(_DBA_JURISDICTION.keys()),
        }

    entry = _DBA_JURISDICTION.get(state)
    if not entry:
        return {
            "ok": False,
            "error": f"unknown state: {state_raw!r}. Use a 2-letter code or full name.",
            "supported_codes": sorted(_DBA_JURISDICTION.keys()),
        }
    return {
        "ok": True,
        "state": state,
        "dba_filing_level": entry["level"],
        "state_portal_url": entry["url"] or None,
        "notes": entry["notes"],
        "fix_data_note": (
            "If this URL or filing-level looks wrong, fix it in "
            "`starter_business_agents/business_license_agent/tools.py::_DBA_JURISDICTION`. "
            "Every founder downstream benefits."
        ),
    }


DBA_FILING_JURISDICTION = Tool(
    name="dba_filing_jurisdiction",
    description=(
        "Return where to file a Doing-Business-As / Fictitious Business Name "
        "/ Assumed Name registration for a US state. Level is one of: "
        "'state' (Secretary of State), 'county' (county clerk/recorder), "
        "'city' (city/town clerk), 'state+county' (both), 'not_required'. "
        "Also returns the home-state portal URL (when state-level) and "
        "state-specific notes. Call this whenever a founder is registering "
        "a DBA / trade name in any US state."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "state": {
                "type": "string",
                "description": "US state — 2-letter code (e.g. 'CA', 'TX') or full name.",
            },
        },
        "required": ["state"],
    },
    handler=_dba_filing_jurisdiction,
)


def _state_general_business_license(args: dict) -> dict:
    state_raw = args.get("state") or ""
    state = _normalize_state(state_raw)
    if state is None:
        return {
            "ok": False,
            "error": f"unknown state: {state_raw!r}. Use a 2-letter code or full name.",
        }

    entry = _STATE_GENERAL_LICENSE.get(state)
    if entry:
        return {
            "ok": True,
            "state": state,
            "general_state_license_required": True,
            **entry,
            "note": (
                "This is a GENERAL state-level business license, separate "
                "from industry-specific licenses (food, construction, "
                "professional services, alcohol, etc.) and from city/county "
                "business licenses."
            ),
        }
    return {
        "ok": True,
        "state": state,
        "general_state_license_required": False,
        "note": (
            f"{state} does NOT have a general state-level business "
            "license requirement. The founder may still need: (a) "
            "industry-specific state licenses (food, construction, "
            "alcohol, professions); (b) sales-tax permit if selling "
            "tangible goods; (c) employer registrations if hiring "
            "(SUI, withholding, workers' comp); (d) city/county "
            "business license — these are SEPARATE from the state-"
            "level license and are city/county-specific. Use WebSearch "
            "to identify the founder's city/county license requirements."
        ),
    }


STATE_GENERAL_BUSINESS_LICENSE = Tool(
    name="state_general_business_license",
    description=(
        "Return whether a US state has a GENERAL state-level business "
        "license requirement (most do NOT — only AK, DE, HI, NV, WA). "
        "If yes, returns the license name, application URL, and "
        "approximate annual fee. If no, returns guidance on what other "
        "licenses still apply (industry-specific, sales tax, employer, "
        "city/county). Always call this for the founder's state of "
        "operation."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "state": {
                "type": "string",
                "description": "US state — 2-letter code or full name.",
            },
        },
        "required": ["state"],
    },
    handler=_state_general_business_license,
)


def all_tools() -> list[Tool]:
    return [DBA_FILING_JURISDICTION, STATE_GENERAL_BUSINESS_LICENSE]
