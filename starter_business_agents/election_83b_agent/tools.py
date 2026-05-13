# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tools for the 83(b) Election Agent.

Two deterministic tools, no LLM-fabricated dates or addresses:

  * `eighty_three_b_deadline_check` — given the grant date and today's date,
    return days remaining, postmark-by date, and an urgency level. The
    statutory rule under Reg. §1.83-2 is: postmarked within 30 calendar days
    of the property transfer date.

  * `irs_service_center_for_state` — return the IRS service-center mailing
    address based on the founder's state of residence. The §83(b) goes to
    the same center where the taxpayer files Form 1040. The IRS publishes
    the official mapping at
    https://www.irs.gov/filing/where-to-file-your-taxes-for-form-1040 —
    we surface a current snapshot and always link the IRS source so the
    founder verifies before mailing.
"""
from __future__ import annotations

import datetime as dt

from core import Tool


# Snapshot of "Where to File Your Taxes for Form 1040" (no payment enclosed)
# per IRS publication, last verified at module-author timestamp. Founders are
# instructed in every response to verify on irs.gov before postmarking.
#
# Two centers cover the country for paper Form 1040 without payment:
#   - Department of the Treasury, Internal Revenue Service, Kansas City, MO 64999-0002
#   - Department of the Treasury, Internal Revenue Service, Ogden, UT 84201-0002
_KANSAS_CITY = (
    "Department of the Treasury\nInternal Revenue Service\nKansas City, MO 64999-0002"
)
_OGDEN = (
    "Department of the Treasury\nInternal Revenue Service\nOgden, UT 84201-0002"
)
_AUSTIN = (
    "Department of the Treasury\nInternal Revenue Service\nAustin, TX 73301-0002"
)

# State -> (address, source-note). Mapping reflects the IRS routing for paper
# Form 1040 without payment as of the most recent IRS update at module write
# time. The IRS reroutes service centers periodically; the agent must always
# direct the founder to verify on the IRS lookup page.
_STATE_TO_CENTER: dict[str, str] = {
    # Kansas City group (the broad majority — most of the Midwest, South, Northeast)
    **{
        code: _KANSAS_CITY
        for code in (
            "AL", "AR", "CT", "DE", "DC", "FL", "GA", "IL", "IN", "IA", "KS",
            "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "NE", "NH",
            "NJ", "NY", "NC", "ND", "OH", "OK", "PA", "RI", "SC", "SD", "TN",
            "VT", "VA", "WV", "WI",
        )
    },
    # Ogden group (most of the West + Texas)
    **{
        code: _OGDEN
        for code in (
            "AK", "AZ", "CA", "CO", "HI", "ID", "MT", "NV", "NM", "OR", "TX",
            "UT", "WA", "WY",
        )
    },
}

_IRS_LOOKUP_URL = "https://www.irs.gov/filing/where-to-file-your-taxes-for-form-1040"
_IRS_E_FILE_URL = "https://www.irs.gov/forms-pubs/about-form-15620"
_REV_PROC_URL = "https://www.irs.gov/pub/irs-drop/rp-12-29.pdf"


def _eighty_three_b_deadline_check(args: dict) -> dict:
    """Return urgency + postmark-by date for a §83(b) election."""
    grant_date_raw = (args.get("grant_date") or "").strip()
    today_raw = (args.get("today") or "").strip()
    try:
        grant = dt.date.fromisoformat(grant_date_raw)
    except ValueError:
        return {
            "ok": False,
            "error": (
                f"grant_date must be ISO 8601 (YYYY-MM-DD); got {grant_date_raw!r}"
            ),
        }
    if today_raw:
        try:
            today = dt.date.fromisoformat(today_raw)
        except ValueError:
            return {
                "ok": False,
                "error": f"today must be ISO 8601 (YYYY-MM-DD); got {today_raw!r}",
            }
    else:
        today = dt.date.today()

    postmark_by = grant + dt.timedelta(days=30)
    days_remaining = (postmark_by - today).days

    if days_remaining < 0:
        urgency = "EXPIRED"
        recommendation = (
            "The 30-day statutory window has passed. The election cannot be "
            "filed late as of right. Discuss with a CPA / tax attorney "
            "whether a §9100 relief request is available — it is "
            "discretionary and rarely granted."
        )
    elif days_remaining <= 3:
        urgency = "URGENT"
        recommendation = (
            "Mail today by USPS certified mail with return receipt. "
            "Do not rely on the next business day."
        )
    elif days_remaining <= 10:
        urgency = "NEAR"
        recommendation = (
            "Postmark this week. Use USPS certified mail with return receipt "
            "(or IRS Form 15620 to e-file)."
        )
    else:
        urgency = "OK"
        recommendation = (
            "You have time. Don't sit on it — mail or e-file within the "
            "next 7 days to leave a buffer."
        )

    return {
        "ok": True,
        "grant_date": grant.isoformat(),
        "today": today.isoformat(),
        "postmark_by": postmark_by.isoformat(),
        "days_remaining": days_remaining,
        "urgency": urgency,
        "recommendation": recommendation,
        "e_file_option_url": _IRS_E_FILE_URL,
        "model_election_text_source": _REV_PROC_URL,
    }


EIGHTY_THREE_B_DEADLINE_CHECK = Tool(
    name="eighty_three_b_deadline_check",
    description=(
        "Compute the §83(b) postmark deadline and urgency for a given grant "
        "date. Returns the postmark-by date (grant date + 30 calendar days), "
        "days remaining, urgency level (URGENT / NEAR / OK / EXPIRED), and "
        "the URL of the IRS Form 15620 e-file option. Call this FIRST in "
        "every response so the deadline framing is grounded in real dates, "
        "not the model's guess."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "grant_date": {
                "type": "string",
                "description": "ISO 8601 date of stock grant / property transfer (YYYY-MM-DD).",
            },
            "today": {
                "type": "string",
                "description": (
                    "Optional ISO 8601 'today' date for testing. Omit in normal use "
                    "— the tool will use the real current date."
                ),
            },
        },
        "required": ["grant_date"],
    },
    handler=_eighty_three_b_deadline_check,
)


def _irs_service_center_for_state(args: dict) -> dict:
    """Return the IRS service-center address for a US state."""
    state = (args.get("state") or "").strip().upper()
    if not state:
        return {"ok": False, "error": "state is required (2-letter code)."}
    # Accept full names too (just the most common).
    aliases = {"CALIFORNIA": "CA", "TEXAS": "TX", "NEW YORK": "NY", "FLORIDA": "FL"}
    state = aliases.get(state, state)

    center = _STATE_TO_CENTER.get(state)
    if not center:
        return {
            "ok": False,
            "error": (
                f"No known service center for state {state!r}. Verify on the "
                "IRS lookup page below."
            ),
            "irs_lookup_url": _IRS_LOOKUP_URL,
        }
    return {
        "ok": True,
        "state": state,
        "irs_service_center_address": center,
        "irs_lookup_url": _IRS_LOOKUP_URL,
        "verify_note": (
            "The IRS reroutes service centers periodically. Verify this "
            "address on the IRS lookup page above before postmarking — "
            "addresses returned here are a snapshot, not authoritative."
        ),
    }


IRS_SERVICE_CENTER_FOR_STATE = Tool(
    name="irs_service_center_for_state",
    description=(
        "Return the IRS service-center mailing address for the founder's "
        "state of residence. The §83(b) election goes to the same center "
        "where they file Form 1040 (without payment). Always returns the "
        "IRS lookup URL so the founder can verify before mailing — addresses "
        "do change."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "state": {
                "type": "string",
                "description": "US state — 2-letter code preferred (e.g. 'CA', 'TX').",
            },
        },
        "required": ["state"],
    },
    handler=_irs_service_center_for_state,
)


def all_tools() -> list[Tool]:
    return [EIGHTY_THREE_B_DEADLINE_CHECK, IRS_SERVICE_CENTER_FOR_STATE]
