# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Compliance & Tax Setup Agent."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from core import merge_company
from core.ui import (
    REQ,
    UNSET,
    company_loader,
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

profile = company_loader(key="compliance_tax")

# Map a loaded entity_type onto this form's options when it matches.
_ENTITY_OPTIONS = [
    UNSET,
    "Single-member LLC",
    "Multi-member LLC",
    "S-Corp",
    "C-Corp",
    "Sole Proprietor",
    "Partnership",
]
_entity_default = next(
    (i for i, o in enumerate(_ENTITY_OPTIONS)
     if profile and profile.entity_type and profile.entity_type.lower() in o.lower()),
    0,
)

with st.form("compliance_form"):
    col1, col2 = st.columns(2)
    with col1:
        entity = st.selectbox("Entity type" + REQ, _ENTITY_OPTIONS, index=_entity_default)
        formation_state = st.text_input(
            "State of formation" + REQ,
            value=(profile.state_of_formation if profile else ""),
            placeholder="Delaware",
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

    company = merge_company(
        profile,
        entity_type=entity,
        state_of_formation=formation_state.strip(),
        employees_plan=employees,
        notes=(
            f"Entity type: {entity}. State of formation: {formation_state.strip()}. "
            f"States of operation: {operation_states.strip()}. "
            f"Sales channels: {sales_channels.strip()}. Employees: {employees}. "
            f"Expected year 1 revenue: {revenue}. "
            f"Products / services: {products.strip()}"
        ),
    )
    with st.spinner("Mapping compliance..."):
        result = asyncio.run(run(company))

    result_actions(markdown=result, filename="compliance_plan.md", position="top")
    st.markdown(result)
    st.divider()
    result_actions(markdown=result, filename="compliance_plan.md", position="bottom")
