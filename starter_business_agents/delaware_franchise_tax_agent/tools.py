# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tools for the Delaware Franchise Tax Calculator agent.

Delaware computes corporate franchise tax under TWO methods. The state's
billing system defaults to the Authorized Shares method, which produces
eye-popping bills for early-stage startups with high authorized-share
counts. Most C-corps qualify for, but never select, the Assumed Par
Value Capital method, which is typically $400.

This tool computes BOTH methods deterministically. No LLM math.

Source: Delaware Division of Corporations.
  - Tax calculation guide:  https://corp.delaware.gov/frtaxcalc/
  - Pay franchise tax:      https://corp.delaware.gov/paytaxes/
  - File annual report:     https://corp.delaware.gov/paytaxes/
  - Statute:                8 Del. C. §§ 501-507
"""
from __future__ import annotations

import math

from core import Tool


# Delaware franchise tax constants for C-corporations.
# Verified against https://corp.delaware.gov/frtaxcalc/ at module-author time.
_AUTH_SHARES_TIER_0_MAX = 5_000        # 1 – 5,000 authorized shares
_AUTH_SHARES_TIER_0_TAX = 175.0
_AUTH_SHARES_TIER_1_MAX = 10_000       # 5,001 – 10,000
_AUTH_SHARES_TIER_1_TAX = 250.0
_AUTH_SHARES_TIER_INCREMENT = 10_000   # every 10,000 over 10,000
_AUTH_SHARES_TIER_INCREMENT_TAX = 85.0
_APVC_PER_MILLION = 400.0              # $400 per $1M of assumed par value capital
_MIN_TAX = 400.0                       # statutory minimum under APVC method
_MAX_TAX = 200_000.0                   # statutory maximum, either method
_ANNUAL_REPORT_FEE = 50.0              # filed alongside the franchise tax
_DE_PAY_URL = "https://corp.delaware.gov/paytaxes/"
_DE_CALC_URL = "https://corp.delaware.gov/frtaxcalc/"
_LLC_FLAT_TAX_URL = "https://corp.delaware.gov/llctax/"
_LLC_FLAT_TAX = 300.0                  # DE LLCs pay a flat $300/year; due June 1.


def _authorized_shares_method(authorized_shares: int) -> float:
    """Delaware Authorized Shares method — the eye-popping default."""
    if authorized_shares <= _AUTH_SHARES_TIER_0_MAX:
        tax = _AUTH_SHARES_TIER_0_TAX
    elif authorized_shares <= _AUTH_SHARES_TIER_1_MAX:
        tax = _AUTH_SHARES_TIER_1_TAX
    else:
        over = authorized_shares - _AUTH_SHARES_TIER_1_MAX
        # Each additional 10,000 (or portion thereof) adds $85.
        increments = math.ceil(over / _AUTH_SHARES_TIER_INCREMENT)
        tax = _AUTH_SHARES_TIER_1_TAX + (increments * _AUTH_SHARES_TIER_INCREMENT_TAX)
    return min(tax, _MAX_TAX)


def _assumed_par_value_method(
    authorized_shares: int,
    issued_shares: int,
    par_value_per_share: float,
    total_gross_assets: float,
) -> tuple[float, dict]:
    """Delaware Assumed Par Value Capital method — typically much lower.

    Returns (tax, breakdown_for_explanation).

    Algorithm per 8 Del. C. § 503(3):
      1. Assumed par = total_gross_assets / issued_shares
      2. If assumed_par < par_value_per_share, use par_value_per_share instead.
      3. Assumed Par Value Capital = assumed_par * authorized_shares
      4. Round APVC up to the next $1M (or fraction thereof = 1 unit).
      5. Tax = $400 per million.
      6. Floor at $400; cap at $200,000.
    """
    if issued_shares <= 0:
        # Can't divide by zero; APVC method requires at least 1 issued share.
        # Return the floor + a note.
        return _MIN_TAX, {
            "method": "assumed_par_value_capital",
            "note": (
                "issued_shares is 0 — APVC method requires at least 1 issued "
                "share. Returning statutory minimum $400."
            ),
        }
    assumed_par = total_gross_assets / issued_shares
    effective_par = max(assumed_par, par_value_per_share)
    apvc = effective_par * authorized_shares
    millions = math.ceil(apvc / 1_000_000) if apvc > 0 else 0
    tax_before_floor = millions * _APVC_PER_MILLION
    tax = max(_MIN_TAX, min(tax_before_floor, _MAX_TAX))
    return tax, {
        "method": "assumed_par_value_capital",
        "assumed_par_per_share": round(assumed_par, 6),
        "effective_par_per_share": round(effective_par, 6),
        "assumed_par_value_capital": round(apvc, 2),
        "rounded_up_to_millions": millions,
        "tax_before_floor_or_cap": tax_before_floor,
        "tax_after_floor_or_cap": tax,
    }


def _delaware_franchise_tax_calc(args: dict) -> dict:
    """Compute both DE C-Corp methods + recommendation."""
    try:
        authorized = int(args.get("authorized_shares", 0))
        issued = int(args.get("issued_shares", 0))
        par_value = float(args.get("par_value_per_share", 0))
        gross_assets = float(args.get("total_gross_assets", 0))
    except (TypeError, ValueError) as e:
        return {"ok": False, "error": f"all inputs must be numeric: {e}"}

    if authorized <= 0:
        return {
            "ok": False,
            "error": "authorized_shares must be > 0 to compute franchise tax.",
        }
    if par_value < 0 or gross_assets < 0 or issued < 0:
        return {"ok": False, "error": "values must be non-negative."}

    auth_tax = _authorized_shares_method(authorized)
    apvc_tax, apvc_breakdown = _assumed_par_value_method(
        authorized, issued, par_value, gross_assets
    )

    if apvc_tax < auth_tax:
        recommended = "assumed_par_value_capital"
        savings = auth_tax - apvc_tax
    else:
        recommended = "authorized_shares"
        savings = 0.0

    final_tax = min(auth_tax, apvc_tax)
    total_due = final_tax + _ANNUAL_REPORT_FEE

    return {
        "ok": True,
        "inputs": {
            "authorized_shares": authorized,
            "issued_shares": issued,
            "par_value_per_share": par_value,
            "total_gross_assets": gross_assets,
        },
        "authorized_shares_method_tax": auth_tax,
        "assumed_par_value_method_tax": apvc_tax,
        "assumed_par_value_breakdown": apvc_breakdown,
        "recommended_method": recommended,
        "recommended_tax": final_tax,
        "annual_report_fee": _ANNUAL_REPORT_FEE,
        "total_due": total_due,
        "savings_vs_default": savings,
        "pay_url": _DE_PAY_URL,
        "official_calculator_url": _DE_CALC_URL,
        "deadline_note": (
            "Delaware C-Corp franchise tax + annual report due March 1 each "
            "year for the prior calendar year. Penalty for late filing: "
            "$200 + 1.5% monthly interest."
        ),
    }


DELAWARE_FRANCHISE_TAX_CALC = Tool(
    name="delaware_franchise_tax_calc",
    description=(
        "Compute Delaware C-Corp franchise tax under BOTH methods "
        "(Authorized Shares default vs. Assumed Par Value Capital) and "
        "return the recommendation plus dollar savings. Use this whenever "
        "a founder asks about a Delaware franchise tax bill, especially "
        "if the bill looks suspiciously high — the default method bills "
        "early-stage startups $5K-$80K when APVC would bill them $400. "
        "Inputs: authorized_shares (int), issued_shares (int), "
        "par_value_per_share (float, e.g. 0.0001), total_gross_assets "
        "(float, USD, from Form 1120 Schedule L line 15 end-of-year). "
        "Returns both tax amounts, the APVC breakdown showing each "
        "calculation step, the recommended method, total due (including "
        "$50 annual report fee), and the DE pay URL."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "authorized_shares": {
                "type": "integer",
                "description": "Total shares the certificate of incorporation authorizes (look on the COI).",
            },
            "issued_shares": {
                "type": "integer",
                "description": "Total shares actually issued (outstanding) as of December 31 of the tax year.",
            },
            "par_value_per_share": {
                "type": "number",
                "description": "Par value per share from the certificate of incorporation (commonly 0.0001).",
            },
            "total_gross_assets": {
                "type": "number",
                "description": (
                    "Total gross assets in USD per Federal Form 1120 Schedule L, "
                    "end-of-year (line 15). If the company hasn't filed 1120 yet, "
                    "estimate from the year-end balance sheet."
                ),
            },
        },
        "required": [
            "authorized_shares",
            "issued_shares",
            "par_value_per_share",
            "total_gross_assets",
        ],
    },
    handler=_delaware_franchise_tax_calc,
)


def _delaware_llc_flat_tax(args: dict) -> dict:
    """DE LLC + LP + GP pay a flat $300/year due June 1. Just return the facts."""
    return {
        "ok": True,
        "entity_type": args.get("entity_type", "llc"),
        "annual_tax": _LLC_FLAT_TAX,
        "due_date": "June 1",
        "pay_url": _LLC_FLAT_TAX_URL,
        "note": (
            "Delaware LLCs/LPs/GPs pay a flat $300/year — no franchise tax "
            "calculation required, no annual report to file. Just pay $300. "
            "Penalty for late payment is $200 + 1.5% monthly interest."
        ),
    }


DELAWARE_LLC_FLAT_TAX = Tool(
    name="delaware_llc_flat_tax",
    description=(
        "Return the flat $300/year tax info for Delaware LLCs / LPs / GPs. "
        "Call this if the founder is asking about a DE LLC (not a C-Corp) — "
        "the franchise tax math doesn't apply; the entity owes a flat $300 "
        "with no annual report."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "entity_type": {
                "type": "string",
                "description": "One of: llc, lp, gp.",
            },
        },
        "required": [],
    },
    handler=_delaware_llc_flat_tax,
)


def all_tools() -> list[Tool]:
    return [DELAWARE_FRANCHISE_TAX_CALC, DELAWARE_LLC_FLAT_TAX]
