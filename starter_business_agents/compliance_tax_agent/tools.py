# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tools for the Compliance & Tax Setup Agent.

  * `state_compliance_lookup` — given a list of US states the founder
    operates in, return per-state annual-report / franchise-tax URLs, the
    approximate annual fee, the registered-agent reference page, and any
    state-specific notes — plus the federal portal set (IRS, FinCEN BOI,
    SBA). The agent embeds these URLs verbatim in the State Filings and
    Federal Filings sections instead of fabricating them from memory.

  * `generate_compliance_ics` — given a list of upcoming deadline events
    (date + summary + description), emit a valid RFC 5545 .ics calendar
    blob the founder can save and import to Google / Apple / Outlook
    calendar. Replaces LegalZoom's "Compliance Concierge" ($379/yr) —
    we hand the founder a free .ics file with every annual deadline
    pre-loaded.

Per the founder pain-point research: 60% of business reinstatements
stem from missed annual reports. Calendar reminders solve this for free.

Data lives in `core/state_portals.py` (shared across agents). Update there.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import re

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


_ICAL_LINE_LIMIT = 75  # RFC 5545 §3.1 line-length cap


def _escape_ics_text(s: str) -> str:
    """RFC 5545 §3.3.11 text escaping."""
    return (
        s.replace("\\", "\\\\")
        .replace(",", "\\,")
        .replace(";", "\\;")
        .replace("\n", "\\n")
        .replace("\r", "")
    )


def _fold(line: str) -> str:
    """RFC 5545 §3.1 line folding — lines >75 octets get CRLF + leading space."""
    if len(line) <= _ICAL_LINE_LIMIT:
        return line
    chunks = [line[i : i + _ICAL_LINE_LIMIT] for i in range(0, len(line), _ICAL_LINE_LIMIT)]
    return chunks[0] + "".join("\r\n " + c for c in chunks[1:])


def _ics_uid(stamp: str, date: str, summary: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", summary.lower()).strip("-")[:30] or "event"
    digest = hashlib.sha1(f"{stamp}|{date}|{summary}".encode()).hexdigest()[:8]
    return f"{date}-{slug}-{digest}@ai-native-business-apps"


def _generate_compliance_ics(args: dict) -> dict:
    """Emit a valid RFC 5545 .ics blob for a list of compliance deadlines.

    Input: events = [{date, summary, description}, ...]
        date: ISO 8601 YYYY-MM-DD
        summary: short event title (e.g. "DE C-Corp Franchise Tax + Annual Report")
        description: longer body (e.g. "Pay at https://corp.delaware.gov/paytaxes/...")
    """
    events = args.get("events") or []
    if not isinstance(events, list) or not events:
        return {"ok": False, "error": "events must be a non-empty list."}

    now = dt.datetime.utcnow()
    dtstamp = now.strftime("%Y%m%dT%H%M%SZ")

    lines: list[str] = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//ai-native-business-apps//compliance-tax-agent//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Business Compliance Deadlines",
        "X-WR-TIMEZONE:UTC",
    ]

    accepted: list[dict] = []
    rejected: list[dict] = []
    for i, ev in enumerate(events):
        date_raw = (ev.get("date") or "").strip()
        summary_raw = (ev.get("summary") or "").strip()
        description_raw = (ev.get("description") or "").strip()
        if not summary_raw:
            rejected.append({"index": i, "reason": "summary missing", "input": ev})
            continue
        try:
            date = dt.date.fromisoformat(date_raw)
        except ValueError:
            rejected.append(
                {"index": i, "reason": f"date not ISO 8601: {date_raw!r}", "input": ev}
            )
            continue

        dtstart = date.strftime("%Y%m%d")
        dtend = (date + dt.timedelta(days=1)).strftime("%Y%m%d")
        uid = _ics_uid(dtstamp, dtstart, summary_raw)
        summary_esc = _escape_ics_text(summary_raw)
        desc_esc = _escape_ics_text(description_raw)

        event_lines = [
            "BEGIN:VEVENT",
            _fold(f"UID:{uid}"),
            f"DTSTAMP:{dtstamp}",
            f"DTSTART;VALUE=DATE:{dtstart}",
            f"DTEND;VALUE=DATE:{dtend}",
            _fold(f"SUMMARY:{summary_esc}"),
        ]
        if desc_esc:
            event_lines.append(_fold(f"DESCRIPTION:{desc_esc}"))
        event_lines.extend(
            [
                "STATUS:CONFIRMED",
                "TRANSP:OPAQUE",
                "BEGIN:VALARM",
                "ACTION:DISPLAY",
                _fold(f"DESCRIPTION:Reminder: {summary_esc} (7 days out)"),
                "TRIGGER:-P7D",
                "END:VALARM",
                "END:VEVENT",
            ]
        )
        lines.extend(event_lines)
        accepted.append({"date": dtstart, "summary": summary_raw})

    lines.append("END:VCALENDAR")
    ics_blob = "\r\n".join(lines) + "\r\n"

    return {
        "ok": True,
        "ics_content": ics_blob,
        "events_added": len(accepted),
        "events_rejected": len(rejected),
        "accepted": accepted,
        "rejected": rejected,
        "filename_suggestion": "business-compliance-deadlines.ics",
        "import_instructions": (
            "Save the ics_content to a file named "
            "'business-compliance-deadlines.ics' and import it: "
            "Google Calendar → Settings → Import & export → Import; "
            "Apple Calendar → File → Import; "
            "Outlook → File → Open & Export → Import/Export → Import an "
            "iCalendar (.ics) file. Every event gets a 7-day-out reminder "
            "by default."
        ),
    }


GENERATE_COMPLIANCE_ICS = Tool(
    name="generate_compliance_ics",
    description=(
        "Emit a valid RFC 5545 .ics calendar file (as a string) for a "
        "list of compliance deadlines. Every event gets a 7-day-out "
        "VALARM reminder. Call this ONCE at the end of your response "
        "after you've identified all the federal + state + local annual "
        "filing deadlines from the founder's situation. The output is "
        "embedded directly in your response so the founder can copy-paste "
        "into a .ics file. Replaces LegalZoom's Compliance Concierge "
        "($379/yr) for the reminder part."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "events": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "ISO 8601 YYYY-MM-DD deadline date.",
                        },
                        "summary": {
                            "type": "string",
                            "description": (
                                "Short event title (e.g. 'DE C-Corp Franchise Tax + Annual Report')."
                            ),
                        },
                        "description": {
                            "type": "string",
                            "description": (
                                "Longer description with payment URL and any context. "
                                "Newlines OK."
                            ),
                        },
                    },
                    "required": ["date", "summary"],
                },
                "description": "List of upcoming compliance deadlines.",
            },
        },
        "required": ["events"],
    },
    handler=_generate_compliance_ics,
)


def all_tools() -> list[Tool]:
    return [STATE_COMPLIANCE_LOOKUP, GENERATE_COMPLIANCE_ICS]
