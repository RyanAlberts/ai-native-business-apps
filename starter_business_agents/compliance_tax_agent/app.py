# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Compliance & Tax Setup Agent."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from core.ui import (
    REQ,
    UNSET,
    inject_styles,
    result_actions,
    sticky_header,
    validate_required,
)

from starter_business_agents.compliance_tax_agent.agent import run  # noqa


st.set_page_config(page_title="Compliance & Tax Setup", page_icon="📋", layout="centered")

inject_styles()
sticky_header(
    emoji="📋",
    title="Compliance & Tax Setup Agent",
    caption="Sales-tax nexus, state registrations, annual filings, bookkeeping — pre-CPA.",
)

with st.form("compliance_form"):
    col1, col2 = st.columns(2)
    with col1:
        entity = st.selectbox(
            "Entity type" + REQ,
            [
                UNSET,
                "Single-member LLC",
                "Multi-member LLC",
                "S-Corp",
                "C-Corp",
                "Sole Proprietor",
                "Partnership",
            ],
        )
        formation_state = st.text_input(
            "State of formation" + REQ, placeholder="Delaware"
        )
        revenue = st.selectbox(
            "Year 1 revenue (expected)" + REQ,
            [UNSET, "<$50k", "$50k–$250k", "$250k–$1M", "$1M+"],
        )
    with col2:
        operation_states = st.text_input(
            "States where you operate / have presence" + REQ,
            placeholder="California, Texas",
        )
        sales_channels = st.text_input(
            "How you sell" + REQ,
            placeholder="Shopify own site + Amazon FBA + Etsy",
        )
        employees = st.selectbox(
            "Employees / payroll" + REQ,
            [UNSET, "No employees", "1–5 W-2", "5+ W-2", "1099 contractors only"],
        )

    products = st.text_area(
        "What you sell + customer locations" + REQ,
        placeholder=(
            "e.g. skincare products to customers in all 50 states; tangible goods, "
            "no services; inventory at CA 3PL + Amazon FBA"
        ),
        height=100,
    )

    submitted = st.form_submit_button("Create compliance plan", type="primary")

if submitted:
    validate_required(
        {
            "Entity type": entity,
            "State of formation": formation_state,
            "Year 1 revenue (expected)": revenue,
            "States where you operate / have presence": operation_states,
            "How you sell": sales_channels,
            "Employees / payroll": employees,
            "What you sell + customer locations": products,
        }
    )

    full_input = (
        f"Entity type: {entity}\n"
        f"State of formation: {formation_state.strip()}\n"
        f"States of operation: {operation_states.strip()}\n"
        f"Sales channels: {sales_channels.strip()}\n"
        f"Employees: {employees}\n"
        f"Expected year 1 revenue: {revenue}\n\n"
        f"Products / services: {products.strip()}"
    )
    with st.spinner("Mapping compliance..."):
        result = asyncio.run(run(full_input))

    result_actions(markdown=result, filename="compliance_plan.md", position="top")
    st.markdown(result)
    st.divider()
    result_actions(markdown=result, filename="compliance_plan.md", position="bottom")
