# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Bank & Insurance Setup Agent."""
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

from starter_business_agents.bank_insurance_agent.agent import run  # noqa


st.set_page_config(page_title="Bank & Insurance Setup", page_icon="🏦", layout="centered")

inject_styles()
sticky_header(
    emoji="🏦",
    title="Bank & Insurance Setup Agent",
    caption="A business bank pick, the insurance you actually need, and a 30-day plan.",
)

with st.form("bank_insurance_form"):
    col1, col2 = st.columns(2)
    with col1:
        business = st.text_input(
            "Business (name + what it does)" + REQ,
            placeholder="Acme Labs LLC — SaaS for clinics",
        )
        state = st.text_input("State of operation" + REQ, placeholder="California")
        stage = st.selectbox(
            "Stage" + REQ,
            [UNSET, "Pre-revenue", "<$100k/yr", "$100k–$1M/yr", "$1M+/yr"],
        )
    with col2:
        employees = st.selectbox(
            "Employees" + REQ,
            [
                UNSET,
                "Just founders",
                "1–5 employees",
                "6–25 employees",
                "25+ employees",
            ],
        )
        physical = st.selectbox(
            "Physical space" + REQ,
            [
                UNSET,
                "Fully remote",
                "Co-working / shared",
                "Leased office",
                "Owned property",
                "Retail / customer-facing",
            ],
        )
        data = st.selectbox(
            "Customer data sensitivity" + REQ,
            [
                UNSET,
                "None / minimal",
                "Email + contact info",
                "Payment info (Stripe-handled)",
                "PII (names, addresses)",
                "PHI / regulated",
            ],
        )

    description = st.text_area(
        "Anything else — vehicles, advice-based services, regulated industry, etc." + REQ,
        placeholder="e.g. we give technical advice to clinics; we have a company car; we sometimes work on-site",
        height=100,
    )

    submitted = st.form_submit_button("Create bank + insurance plan", type="primary")

if submitted:
    validate_required(
        {
            "Business (name + what it does)": business,
            "State of operation": state,
            "Stage": stage,
            "Employees": employees,
            "Physical space": physical,
            "Customer data sensitivity": data,
            "Anything else": description,
        }
    )

    full_input = (
        f"Business: {business.strip()}\n"
        f"State of operation: {state.strip()}\n"
        f"Stage: {stage}\n"
        f"Employees: {employees}\n"
        f"Physical space: {physical}\n"
        f"Customer data: {data}\n\n"
        f"Additional context: {description.strip()}"
    )
    with st.spinner("Building plan..."):
        result = asyncio.run(run(full_input))

    result_actions(markdown=result, filename="bank_insurance_plan.md", position="top")
    st.markdown(result)
    st.divider()
    result_actions(markdown=result, filename="bank_insurance_plan.md", position="bottom")
