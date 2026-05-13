# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Worker Classification Agent."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from starter_business_agents.worker_classification_agent.agent import run


st.set_page_config(page_title="Worker Classification Agent", page_icon="👥")
st.title("👥 Worker Classification Agent — 1099 or W-2?")
st.caption(
    "40% of small businesses get hit with payroll misclassification "
    "findings. Calling someone a 'contractor' doesn't make them one. "
    "This agent applies the IRS + DOL 2024 + state-specific tests "
    "(AB5, MA, NJ) and gives you a verdict + risk score + the right "
    "contract type to issue. Free + open source."
)

with st.form("inputs"):
    role = st.text_input(
        "Role / job title",
        placeholder="e.g. Senior software engineer / brand designer / sales rep",
    )
    state = st.text_input(
        "State where work will be performed (2-letter)",
        value="CA",
        max_chars=2,
    ).upper()
    cols = st.columns(2)
    with cols[0]:
        hours = st.selectbox(
            "Hours / schedule",
            options=[
                "Full-time (35-40+ hours/week)",
                "Part-time (10-30 hours/week)",
                "Project-based / hours vary",
                "On-demand / sporadic",
            ],
        )
        duration = st.selectbox(
            "Duration",
            options=[
                "Open-ended / indefinite",
                "Long-term (6+ months)",
                "Specific project (1-6 months)",
                "Short-term (<1 month)",
            ],
        )
        equipment = st.selectbox(
            "Equipment",
            options=[
                "Company provides laptop and tools",
                "Worker uses their own equipment",
                "Mixed",
            ],
        )
    with cols[1]:
        payment = st.selectbox(
            "Payment structure",
            options=[
                "Hourly",
                "Salaried (annual)",
                "Flat fee per project",
                "Flat fee per deliverable",
                "Other / mixed",
            ],
        )
        other_clients = st.selectbox(
            "Does worker have other clients / their own business?",
            options=[
                "No — works only for us",
                "Yes — has other clients / independent business",
                "Unknown / unclear",
            ],
        )
        benefits = st.selectbox(
            "Benefits offered (health, PTO, retirement)?",
            options=["No benefits", "Some benefits", "Full benefits"],
        )
    is_core = st.checkbox(
        "Is this role core to the business? (e.g. 'we're a software "
        "company and this person writes our software')",
        value=True,
    )
    extra = st.text_area(
        "Anything else (current contract type, founder concern, etc.)?",
        placeholder="e.g. 'we want to call them 1099 to avoid payroll burden'",
        height=80,
    )

    submitted = st.form_submit_button("Classify the role", type="primary")

if submitted:
    if not role:
        st.error("Role is required.")
    else:
        prompt = (
            f"Role: {role}.\n"
            f"State where work will be performed: {state}.\n"
            f"Hours: {hours}.\n"
            f"Duration: {duration}.\n"
            f"Equipment: {equipment}.\n"
            f"Payment structure: {payment}.\n"
            f"Other clients: {other_clients}.\n"
            f"Benefits offered: {benefits}.\n"
            f"Is role core to the business: {'Yes' if is_core else 'No'}.\n"
            f"Additional context: {extra or '(none)'}"
        )
        with st.spinner("Applying IRS + DOL + state tests..."):
            result = asyncio.run(run(prompt))
        st.markdown(result)
        st.download_button(
            "Download analysis (markdown)",
            result,
            file_name=f"classification-{role.replace(' ', '-')}.md",
        )
