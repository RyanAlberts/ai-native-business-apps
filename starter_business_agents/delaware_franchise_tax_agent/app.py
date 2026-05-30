# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Delaware Franchise Tax Calculator."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from core import merge_company
from core.ui import (
    REQ,
    company_loader,
    inject_styles,
    result_actions,
    sticky_header,
)

from starter_business_agents.delaware_franchise_tax_agent.agent import run  # noqa


st.set_page_config(
    page_title="DE Franchise Tax Calculator", page_icon="🏛️", layout="centered"
)

inject_styles()
sticky_header(
    emoji="🏛️",
    title="Delaware Franchise Tax Calculator",
    caption=(
        "Got a $5K–$85K Delaware franchise tax bill? Almost certainly the wrong "
        "(default) method. This recomputes under both methods and tells you "
        "which to elect on March 1. Free — replaces Carta / LegalZoom for this."
    ),
)

profile = company_loader(key="delaware_franchise")

entity_type = st.radio(
    "Entity type" + REQ,
    options=["C-Corp / S-Corp", "LLC / LP / GP"],
    horizontal=True,
)

# ── LLC path — flat $300 fee, single button ───────────────────────────
if entity_type.startswith("LLC"):
    if st.button("Create my LLC tax answer", type="primary"):
        llc_q = "I'm a Delaware LLC. What do I owe?"
        agent_input = merge_company(profile, notes=llc_q) if profile else llc_q
        with st.spinner("Computing..."):
            result = asyncio.run(run(agent_input))

        result_actions(
            markdown=result, filename="de-franchise-tax-llc.md", position="top"
        )
        st.markdown(result)
        st.divider()
        result_actions(
            markdown=result, filename="de-franchise-tax-llc.md", position="bottom"
        )

# ── C-Corp / S-Corp path — full form ─────────────────────────────────
else:
    with st.form("franchise_tax_form"):
        cols = st.columns(2)
        with cols[0]:
            authorized = st.number_input(
                "Authorized shares (from your COI)" + REQ,
                min_value=1,
                value=10_000_000,
                step=1,
            )
            issued = st.number_input(
                "Issued / outstanding shares (Dec 31)" + REQ,
                min_value=0,
                value=8_000_000,
                step=1,
            )
        with cols[1]:
            par = st.number_input(
                "Par value per share ($)" + REQ,
                min_value=0.0,
                value=0.0001,
                step=0.0001,
                format="%.4f",
            )
            assets = st.number_input(
                "Total gross assets ($, year-end, Form 1120 Schedule L line 15)" + REQ,
                min_value=0.0,
                value=50_000.0,
                step=1000.0,
            )
        bill_received = st.text_input(
            "Optional: the bill amount DE sent you ($) — for context",
            value="",
            placeholder="e.g. 85165",
            help="Optional. Leave blank if you haven't received a bill yet.",
        )
        submitted = st.form_submit_button(
            "Create tax recomputation (both methods)", type="primary"
        )

    if submitted:
        bill_clause = (
            f" The bill Delaware sent me is ${bill_received.strip()}."
            if bill_received.strip()
            else ""
        )
        prompt = (
            f"Delaware C-Corp. Authorized: {authorized:,} shares. "
            f"Issued: {issued:,} shares. Par value: ${par:.4f}/share. "
            f"Total gross assets at year-end: ${assets:,.2f}.{bill_clause}"
        )
        agent_input = merge_company(profile, notes=prompt) if profile else prompt
        with st.spinner("Recomputing under both methods..."):
            result = asyncio.run(run(agent_input))

        result_actions(
            markdown=result, filename="de-franchise-tax-corp.md", position="top"
        )
        st.markdown(result)
        st.divider()
        result_actions(
            markdown=result, filename="de-franchise-tax-corp.md", position="bottom"
        )
