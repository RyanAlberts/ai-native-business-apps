# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Delaware Franchise Tax Calculator."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from starter_business_agents.delaware_franchise_tax_agent.agent import run


st.set_page_config(page_title="DE Franchise Tax Calculator", page_icon="🏛️")
st.title("🏛️ Delaware Franchise Tax Calculator")
st.caption(
    "Got a $5K–$85K Delaware franchise tax bill? You're almost certainly "
    "paying the wrong (default) method. This agent recomputes under both "
    "methods and tells you which to elect on your March 1 filing. Free + "
    "open source. Replaces what Carta/LegalZoom charge to fix."
)

entity_type = st.radio(
    "Entity type",
    options=["C-Corp / S-Corp", "LLC / LP / GP"],
    horizontal=True,
)

if entity_type.startswith("LLC"):
    if st.button("Show me what I owe", type="primary"):
        with st.spinner("Computing..."):
            result = asyncio.run(run("I'm a Delaware LLC. What do I owe?"))
        st.markdown(result)
else:
    with st.form("inputs"):
        cols = st.columns(2)
        with cols[0]:
            authorized = st.number_input(
                "Authorized shares (from your COI)",
                min_value=1,
                value=10_000_000,
                step=1,
            )
            issued = st.number_input(
                "Issued / outstanding shares (Dec 31)",
                min_value=0,
                value=8_000_000,
                step=1,
            )
        with cols[1]:
            par = st.number_input(
                "Par value per share ($)",
                min_value=0.0,
                value=0.0001,
                step=0.0001,
                format="%.4f",
            )
            assets = st.number_input(
                "Total gross assets ($, year-end, Form 1120 Schedule L line 15)",
                min_value=0.0,
                value=50_000.0,
                step=1000.0,
            )
        bill_received = st.text_input(
            "Optional: the bill amount DE sent you ($) — for context",
            value="",
            placeholder="e.g. 85165",
        )
        submitted = st.form_submit_button("Recompute under both methods", type="primary")

    if submitted:
        bill_clause = f" The bill Delaware sent me is ${bill_received}." if bill_received else ""
        prompt = (
            f"Delaware C-Corp. Authorized: {authorized:,} shares. "
            f"Issued: {issued:,} shares. Par value: ${par:.4f}/share. "
            f"Total gross assets at year-end: ${assets:,.2f}.{bill_clause}"
        )
        with st.spinner("Recomputing under both methods..."):
            result = asyncio.run(run(prompt))
        st.markdown(result)
