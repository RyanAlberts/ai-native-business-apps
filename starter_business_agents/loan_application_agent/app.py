# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Loan & Funding Application Agent."""
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

from starter_business_agents.loan_application_agent.agent import run  # noqa


st.set_page_config(
    page_title="Loan & Funding Application Agent", page_icon="💰", layout="centered"
)

inject_styles()
sticky_header(
    emoji="💰",
    title="Loan & Funding Application Agent",
    caption="Match your business to SBA loans, microloans, grants, and CDFI programs.",
)

with st.form("loan_form"):
    col1, col2 = st.columns(2)
    with col1:
        business = st.text_input(
            "Business (name + what it does)" + REQ,
            placeholder="Acme Bakery — wholesale + retail",
        )
        state = st.text_input("State / city" + REQ, placeholder="Boise, Idaho")
        stage = st.selectbox(
            "Stage" + REQ,
            [UNSET, "Pre-revenue", "<$100k/yr revenue", "$100k–$1M/yr", "$1M+/yr"],
        )
    with col2:
        need = st.text_input("Amount needed" + REQ, placeholder="$120,000")
        purpose = st.selectbox(
            "Use of funds" + REQ,
            [
                UNSET,
                "Working capital",
                "Equipment",
                "Real estate",
                "Inventory",
                "Growth/hiring",
                "Mixed",
            ],
        )
        credit = st.selectbox(
            "Founder credit score range" + REQ,
            [
                UNSET,
                "Don't know / decline to say",
                "<620",
                "620–680",
                "680–720",
                "720–760",
                "760+",
            ],
        )

    description = st.text_area(
        "Additional context (collateral, existing debt, urgency, etc.)" + REQ,
        placeholder="e.g. founder owns home with $120k equity, no other business debt, want funded within 60 days",
        height=120,
    )

    submitted = st.form_submit_button("Create funding plan", type="primary")

if submitted:
    validate_required(
        {
            "Business (name + what it does)": business,
            "State / city": state,
            "Stage": stage,
            "Amount needed": need,
            "Use of funds": purpose,
            "Founder credit score range": credit,
            "Additional context": description,
        }
    )

    full_input = (
        f"Business: {business.strip()}\n"
        f"Location: {state.strip()}\n"
        f"Stage: {stage}\n"
        f"Funding need: {need.strip()}\n"
        f"Use of funds: {purpose}\n"
        f"Founder credit: {credit}\n\n"
        f"Additional context: {description.strip()}"
    )
    with st.spinner("Researching funding paths..."):
        result = asyncio.run(run(full_input))

    result_actions(markdown=result, filename="funding_plan.md", position="top")
    st.markdown(result)
    st.divider()
    result_actions(markdown=result, filename="funding_plan.md", position="bottom")
