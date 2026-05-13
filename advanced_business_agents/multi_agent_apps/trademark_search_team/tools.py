# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tools for the Trademark Search Team.

One deterministic tool — the USPTO fee estimator. Web research is done
via the WebSearch tool from `allowed_tools` (provider-side), so the
sub-agents can pull real TESS / state / common-law / class-manual data
at run time rather than hallucinating.

USPTO fees change. The amounts below reflect the post-January-2025 fee
schedule. The tool always returns the source URL so the founder can
confirm — and the prompt instructs the synthesizer to direct the founder
there before paying.
"""
from __future__ import annotations

from core import Tool


# Post-Jan-2025 USPTO fee schedule (electronic filing).
# Source: https://www.uspto.gov/trademarks/fees-payment-information
_FEE_USPTO_URL = "https://www.uspto.gov/trademarks/fees-payment-information"
_TEAS_PLUS_PER_CLASS = 250        # base application, TEAS Plus
_TEAS_STANDARD_PER_CLASS = 350    # base application, TEAS Standard
_FEE_INSUFFICIENCY = 100          # surcharge for failing TEAS Plus rules
_FEE_FREE_FORM_ID = 200           # custom goods/services description surcharge
_FEE_STATEMENT_OF_USE = 100       # Statement of Use per class (intent-to-use)
_FEE_EXTENSION_REQUEST = 125      # Extension of Time per class
_FEE_SECTION_8 = 325              # Section 8 declaration year 6
_FEE_SECTION_15 = 250             # Section 15 incontestability declaration
_FEE_SECTION_8_15_COMBO = 425     # Combined §8 + §15 maintenance


def _uspto_fee_estimate(args: dict) -> dict:
    """Estimate the USPTO filing fee for a trademark application.

    Inputs:
        num_classes (int): how many Nice Classification classes to file in
        teas_form (str): "plus" or "standard" (default "plus")
        intent_to_use (bool): if true, add Statement of Use per class
    """
    try:
        n = int(args.get("num_classes", 1))
    except (TypeError, ValueError):
        return {"ok": False, "error": "num_classes must be an integer."}
    if n < 1:
        return {"ok": False, "error": "num_classes must be >= 1."}

    form = (args.get("teas_form") or "plus").strip().lower()
    if form not in ("plus", "standard"):
        return {
            "ok": False,
            "error": "teas_form must be 'plus' or 'standard'.",
        }
    itu = bool(args.get("intent_to_use", False))

    per_class = _TEAS_PLUS_PER_CLASS if form == "plus" else _TEAS_STANDARD_PER_CLASS
    base_fee = per_class * n

    breakdown: list[dict] = [
        {
            "line": f"Base application ({form.upper()}) × {n} class(es) @ ${per_class}",
            "subtotal": base_fee,
        }
    ]
    total = base_fee

    if itu:
        sou = _FEE_STATEMENT_OF_USE * n
        breakdown.append(
            {
                "line": (
                    f"Statement of Use × {n} class(es) @ ${_FEE_STATEMENT_OF_USE} "
                    "(filed within 6 months of allowance, or with extensions)"
                ),
                "subtotal": sou,
            }
        )
        total += sou

    return {
        "ok": True,
        "num_classes": n,
        "teas_form": form,
        "intent_to_use": itu,
        "base_application_per_class": per_class,
        "estimated_total": total,
        "fee_breakdown": breakdown,
        "maintenance_fees_to_plan_for": {
            "section_8_year_6": _FEE_SECTION_8,
            "section_8_15_combo_year_6": _FEE_SECTION_8_15_COMBO,
            "section_8_renewal_year_10": _FEE_SECTION_8,
        },
        "teas_plus_vs_standard_note": (
            f"TEAS Plus is cheaper (${_TEAS_PLUS_PER_CLASS}/class) but requires "
            "using exact pre-approved goods/services descriptions from the "
            "USPTO ID Manual. If the founder's description has to be custom, "
            "they must use TEAS Standard (${0}/class) or pay a ${1} "
            "free-form surcharge.".format(_TEAS_STANDARD_PER_CLASS, _FEE_FREE_FORM_ID)
        ),
        "source_url": _FEE_USPTO_URL,
        "verify_note": (
            "USPTO fees changed January 18, 2025. Verify on the source URL "
            "before paying — fees can change again on October 1 of any year."
        ),
    }


USPTO_FEE_ESTIMATE = Tool(
    name="uspto_fee_estimate",
    description=(
        "Estimate the total USPTO filing fee for a trademark application "
        "across N classes under TEAS Plus or TEAS Standard, with optional "
        "Statement of Use surcharge if filing an intent-to-use application. "
        "Returns a line-itemed breakdown + maintenance fees the founder "
        "should plan for at year 6 and year 10. ALWAYS surfaces the USPTO "
        "fee-page URL so the founder confirms before paying."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "num_classes": {
                "type": "integer",
                "description": "Number of Nice Classification classes to file in.",
            },
            "teas_form": {
                "type": "string",
                "enum": ["plus", "standard"],
                "description": (
                    "TEAS Plus (cheaper, requires pre-approved descriptions) "
                    "or TEAS Standard (more flexible, more expensive)."
                ),
            },
            "intent_to_use": {
                "type": "boolean",
                "description": (
                    "True if filing intent-to-use (mark not yet used in "
                    "commerce). Adds the Statement of Use fee per class."
                ),
            },
        },
        "required": ["num_classes"],
    },
    handler=_uspto_fee_estimate,
)


def all_tools() -> list[Tool]:
    return [USPTO_FEE_ESTIMATE]
