# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Compliance & Tax Setup Agent."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from starter_business_agents.compliance_tax_agent.agent import run  # noqa


st.set_page_config(page_title="Compliance & Tax Setup", page_icon="📋")
st.title("📋 Compliance & Tax Setup Agent")
st.caption(
    "Map sales-tax nexus, state registrations, annual filings, and "
    "bookkeeping — for founders who don't have a CPA yet."
)

col1, col2 = st.columns(2)
with col1:
    entity = st.selectbox(
        "Entity type",
        ["Single-member LLC", "Multi-member LLC", "S-Corp", "C-Corp", "Sole Proprietor", "Partnership"],
    )
    formation_state = st.text_input("State of formation", placeholder="Delaware")
    revenue = st.selectbox("Year 1 revenue (expected)", ["<$50k", "$50k–$250k", "$250k–$1M", "$1M+"])
with col2:
    operation_states = st.text_input(
        "States where you operate / have presence",
        placeholder="California, Texas",
    )
    sales_channels = st.text_input(
        "How you sell",
        placeholder="Shopify own site + Amazon FBA + Etsy",
    )
    employees = st.selectbox(
        "Employees / payroll",
        ["No employees", "1–5 W-2", "5+ W-2", "1099 contractors only"],
    )

products = st.text_area(
    "What you sell + customer locations",
    placeholder=(
        "e.g. skincare products to customers in all 50 states; tangible goods, "
        "no services; inventory at CA 3PL + Amazon FBA"
    ),
    height=100,
)

if st.button("Map compliance plan", type="primary") and products.strip():
    full_input = (
        f"Entity type: {entity}\n"
        f"State of formation: {formation_state or '(not specified)'}\n"
        f"States of operation: {operation_states or '(not specified)'}\n"
        f"Sales channels: {sales_channels or '(not specified)'}\n"
        f"Employees: {employees}\n"
        f"Expected year 1 revenue: {revenue}\n\n"
        f"Products / services: {products.strip()}"
    )
    with st.spinner("Mapping compliance..."):
        result = asyncio.run(run(full_input))
    st.markdown(result)
    st.download_button("Download as markdown", result, file_name="compliance_plan.md")
