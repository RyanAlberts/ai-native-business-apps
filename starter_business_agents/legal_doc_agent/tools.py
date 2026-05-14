# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tools for the Legal Doc Agent.

One deterministic tool — pure date + share math for cofounder
agreements, so the agent never fabricates a vesting schedule or miscounts
months past the cliff. The agent uses the tool whenever the founder
asks for a cofounder agreement or any document that includes vesting.

Why: vesting-cliff math is one of the most-frequently-broken founder
agreements per the founder pain-point research. Founders pick "4 years
with 1-year cliff" from a template, sign, and then can't tell you what
their cap table looks like on a specific date 18 months in.
"""
from __future__ import annotations

import datetime as dt

from core import Tool


def _add_months(d: dt.date, months: int) -> dt.date:
    """Add `months` calendar months to `d`. Clamps to end-of-month."""
    y = d.year + (d.month - 1 + months) // 12
    m = (d.month - 1 + months) % 12 + 1
    # Clamp day to the last valid day of that month.
    next_first = (
        dt.date(y + 1, 1, 1) if m == 12 else dt.date(y, m + 1, 1)
    )
    last_day = (next_first - dt.timedelta(days=1)).day
    return dt.date(y, m, min(d.day, last_day))


def _cofounder_vesting_schedule(args: dict) -> dict:
    """Compute a cofounder's vesting schedule with cliff.

    Inputs (all required except cliff_months which defaults to 12):
        grant_date: ISO 8601 (YYYY-MM-DD) — the start of the vesting period
        total_shares: int — total shares subject to vesting
        vesting_years: int — total vesting duration in years (typically 4)
        cliff_months: int — months before any shares vest (typically 12)
        acceleration_on_change_of_control: str — "none" / "single_trigger" / "double_trigger"
    """
    try:
        grant = dt.date.fromisoformat((args.get("grant_date") or "").strip())
    except (ValueError, TypeError):
        return {
            "ok": False,
            "error": f"grant_date must be ISO YYYY-MM-DD; got {args.get('grant_date')!r}",
        }

    try:
        total = int(args.get("total_shares", 0))
        vesting_years = int(args.get("vesting_years", 4))
        cliff_months = int(args.get("cliff_months", 12))
    except (TypeError, ValueError):
        return {"ok": False, "error": "share counts and months must be integers."}

    if total <= 0:
        return {"ok": False, "error": "total_shares must be > 0."}
    if vesting_years not in (1, 2, 3, 4, 5):
        return {
            "ok": False,
            "error": (
                f"vesting_years must be 1-5 (industry standard is 4); got {vesting_years}"
            ),
        }
    if cliff_months < 0 or cliff_months > vesting_years * 12:
        return {
            "ok": False,
            "error": (
                f"cliff_months must be between 0 and vesting_years × 12 "
                f"({vesting_years * 12}); got {cliff_months}"
            ),
        }

    accel = (args.get("acceleration_on_change_of_control") or "none").strip().lower()
    if accel not in ("none", "single_trigger", "double_trigger"):
        return {
            "ok": False,
            "error": (
                "acceleration_on_change_of_control must be 'none', "
                "'single_trigger', or 'double_trigger'."
            ),
        }

    total_months = vesting_years * 12
    # Shares per post-cliff month (cliff itself vests cliff_months × monthly_amount).
    monthly = total / total_months
    cliff_amount = round(monthly * cliff_months)

    schedule: list[dict] = []
    cumulative = 0
    for m in range(0, total_months + 1):
        date = _add_months(grant, m)
        if m == 0:
            vested = 0
        elif m < cliff_months:
            vested = 0
        elif m == cliff_months:
            vested = cliff_amount
            cumulative = cliff_amount
        else:
            # Post-cliff: vest one month's worth each subsequent month.
            this_month = round(monthly * m) - cumulative
            cumulative += this_month
            vested = this_month
        schedule.append(
            {
                "month": m,
                "date": date.isoformat(),
                "vested_this_period": vested,
                "cumulative_vested": cumulative,
                "remaining": total - cumulative,
            }
        )

    fully_vested_date = _add_months(grant, total_months)
    cliff_date = _add_months(grant, cliff_months)

    accel_note = {
        "none": (
            "No acceleration. On a change of control, unvested shares are "
            "subject to whatever the acquirer / buyer decides — typically "
            "they get cancelled or rolled into a new acquirer-side vesting "
            "schedule. Industry standard for non-founder employees but "
            "RARELY accepted by experienced cofounders."
        ),
        "single_trigger": (
            "100% acceleration on a single trigger (the change of control "
            "itself). All unvested shares vest immediately upon acquisition. "
            "Founder-friendly but acquirer-unfriendly — buyers will often "
            "negotiate this down or insist on re-vesting bonus. Less common "
            "than double-trigger."
        ),
        "double_trigger": (
            "100% acceleration on a DOUBLE trigger: (1) change of control, "
            "AND (2) involuntary termination without cause within 12-24 "
            "months after the acquisition closes. Industry standard for "
            "founder cofounders — balances founder protection with "
            "acquirer's ability to retain talent."
        ),
    }[accel]

    return {
        "ok": True,
        "grant_date": grant.isoformat(),
        "total_shares": total,
        "vesting_years": vesting_years,
        "cliff_months": cliff_months,
        "cliff_date": cliff_date.isoformat(),
        "cliff_amount": cliff_amount,
        "monthly_vest_amount_post_cliff": round(monthly),
        "fully_vested_date": fully_vested_date.isoformat(),
        "schedule": schedule,
        "acceleration_on_change_of_control": accel,
        "acceleration_explanation": accel_note,
        "industry_default_note": (
            "The de facto US startup default is 4-year vesting with a "
            "1-year cliff and double-trigger acceleration on change of "
            "control. Deviating from any of these will draw attention "
            "in Series A diligence."
        ),
    }


COFOUNDER_VESTING_SCHEDULE = Tool(
    name="cofounder_vesting_schedule",
    description=(
        "Compute a cofounder's stock vesting schedule with cliff and "
        "acceleration. Use this WHENEVER drafting a cofounder agreement, "
        "founder restricted-stock purchase agreement, or any document that "
        "embeds a vesting schedule. Returns: cliff date, cliff vesting "
        "amount, monthly vesting amount post-cliff, fully-vested date, a "
        "month-by-month schedule, and an explanation of the change-of-"
        "control acceleration choice. Inputs: grant_date (ISO YYYY-MM-DD), "
        "total_shares (int), vesting_years (1-5; industry default 4), "
        "cliff_months (0-60; industry default 12), "
        "acceleration_on_change_of_control ('none' / 'single_trigger' / "
        "'double_trigger'; industry default 'double_trigger' for "
        "cofounders)."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "grant_date": {
                "type": "string",
                "description": "ISO 8601 date the vesting clock starts (typically the cofounder's start date or incorporation date).",
            },
            "total_shares": {
                "type": "integer",
                "description": "Total shares subject to vesting for this cofounder.",
            },
            "vesting_years": {
                "type": "integer",
                "description": "Total vesting duration in years. Default 4 (industry standard).",
            },
            "cliff_months": {
                "type": "integer",
                "description": "Months before any shares vest. Default 12 (industry standard).",
            },
            "acceleration_on_change_of_control": {
                "type": "string",
                "enum": ["none", "single_trigger", "double_trigger"],
                "description": (
                    "Acceleration trigger for the cofounder. Industry "
                    "default for cofounders: 'double_trigger'."
                ),
            },
        },
        "required": ["grant_date", "total_shares"],
    },
    handler=_cofounder_vesting_schedule,
)


def all_tools() -> list[Tool]:
    return [COFOUNDER_VESTING_SCHEDULE]
