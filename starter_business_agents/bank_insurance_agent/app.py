# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Bank & Insurance Setup Agent."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from starter_business_agents.bank_insurance_agent.agent import run  # noqa


st.set_page_config(page_title="Bank & Insurance Setup", page_icon="🏦")
st.title("🏦 Bank & Insurance Setup Agent")
st.caption(
    "Recommend a business bank account, the insurance policies you actually "
    "need (no upsells), and a 30-day action plan."
)

col1, col2 = st.columns(2)
with col1:
    business = st.text_input("Business (name + what it does)", placeholder="Acme Labs LLC — SaaS for clinics")
    state = st.text_input("State of operation", placeholder="California")
    stage = st.selectbox("Stage", ["Pre-revenue", "<$100k/yr", "$100k–$1M/yr", "$1M+/yr"])
with col2:
    employees = st.selectbox(
        "Employees",
        ["Just founders", "1–5 employees", "6–25 employees", "25+ employees"],
    )
    physical = st.selectbox(
        "Physical space",
        ["Fully remote", "Co-working / shared", "Leased office", "Owned property", "Retail / customer-facing"],
    )
    data = st.selectbox(
        "Customer data sensitivity",
        ["None / minimal", "Email + contact info", "Payment info (Stripe-handled)", "PII (names, addresses)", "PHI / regulated"],
    )

description = st.text_area(
    "Anything else — vehicles, advice-based services, regulated industry, etc.",
    placeholder="e.g. we give technical advice to clinics; we have a company car; we sometimes work on-site",
    height=100,
)

if st.button("Recommend bank + insurance plan", type="primary") and business.strip():
    full_input = (
        f"Business: {business}\n"
        f"State of operation: {state or '(not specified)'}\n"
        f"Stage: {stage}\n"
        f"Employees: {employees}\n"
        f"Physical space: {physical}\n"
        f"Customer data: {data}\n\n"
        f"Additional context: {description.strip() or '(none provided)'}"
    )
    with st.spinner("Building plan..."):
        result = asyncio.run(run(full_input))
    st.markdown(result)
    st.download_button("Download as markdown", result, file_name="bank_insurance_plan.md")
