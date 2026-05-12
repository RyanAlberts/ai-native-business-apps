# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Loan & Funding Application Agent."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from starter_business_agents.loan_application_agent.agent import run  # noqa


st.set_page_config(page_title="Loan & Funding Application Agent", page_icon="💰")
st.title("💰 Loan & Funding Application Agent")
st.caption(
    "Match your business to SBA loans, microloans, grants, and CDFI programs — "
    "and get a checklist for what to gather before applying."
)

col1, col2 = st.columns(2)
with col1:
    business = st.text_input("Business (name + what it does)", placeholder="Acme Bakery — wholesale + retail")
    state = st.text_input("State / city", placeholder="Boise, Idaho")
    stage = st.selectbox("Stage", ["Pre-revenue", "<$100k/yr revenue", "$100k–$1M/yr", "$1M+/yr"])
with col2:
    need = st.text_input("Amount needed", placeholder="$120,000")
    purpose = st.selectbox(
        "Use of funds",
        ["Working capital", "Equipment", "Real estate", "Inventory", "Growth/hiring", "Mixed"],
    )
    credit = st.selectbox(
        "Founder credit score range",
        ["Don't know / decline to say", "<620", "620–680", "680–720", "720–760", "760+"],
    )

description = st.text_area(
    "Additional context (collateral, existing debt, urgency, etc.)",
    placeholder="e.g. founder owns home with $120k equity, no other business debt, want funded within 60 days",
    height=120,
)

if st.button("Find matching funding programs", type="primary") and business.strip():
    full_input = (
        f"Business: {business or '(unnamed)'}\n"
        f"Location: {state or '(not specified)'}\n"
        f"Stage: {stage}\n"
        f"Funding need: {need or '(not specified)'}\n"
        f"Use of funds: {purpose}\n"
        f"Founder credit: {credit}\n\n"
        f"Additional context: {description.strip() or '(none provided)'}"
    )
    with st.spinner("Researching funding paths..."):
        result = asyncio.run(run(full_input))
    st.markdown(result)
    st.download_button("Download as markdown", result, file_name="funding_plan.md")
