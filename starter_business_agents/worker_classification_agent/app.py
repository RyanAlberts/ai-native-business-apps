# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Worker Classification Agent."""
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
    validate_required,
)

from starter_business_agents.worker_classification_agent.agent import run  # noqa


st.set_page_config(
    page_title="Worker Classification Agent", page_icon="👥", layout="centered"
)

inject_styles()
sticky_header(
    emoji="👥",
    title="Worker Classification Agent — 1099 or W-2?",
    caption=(
        "Misclassifying a worker is a common, expensive payroll mistake. "
        "Applies the IRS + DOL economic-reality + state-specific tests (AB5, "
        "MA, NJ) and gives you a verdict + risk score + the right contract type."
    ),
)

profile = company_loader(key="worker_classification")

with st.form("worker_classification_form"):
    role = st.text_input(
        "Role / job title" + REQ,
        placeholder="e.g. Senior software engineer / brand designer / sales rep",
    )
    state = st.text_input(
        "State where work will be performed (2-letter)" + REQ,
        value="CA",
        max_chars=2,
    ).upper()
    cols = st.columns(2)
    with cols[0]:
        hours = st.selectbox(
            "Hours / schedule" + REQ,
            options=[
                "Full-time (35-40+ hours/week)",
                "Part-time (10-30 hours/week)",
                "Project-based / hours vary",
                "On-demand / sporadic",
            ],
        )
        duration = st.selectbox(
            "Duration" + REQ,
            options=[
                "Open-ended / indefinite",
                "Long-term (6+ months)",
                "Specific project (1-6 months)",
                "Short-term (<1 month)",
            ],
        )
        equipment = st.selectbox(
            "Equipment" + REQ,
            options=[
                "Company provides laptop and tools",
                "Worker uses their own equipment",
                "Mixed",
            ],
        )
    with cols[1]:
        payment = st.selectbox(
            "Payment structure" + REQ,
            options=[
                "Hourly",
                "Salaried (annual)",
                "Flat fee per project",
                "Flat fee per deliverable",
                "Other / mixed",
            ],
        )
        other_clients = st.selectbox(
            "Does worker have other clients / their own business?" + REQ,
            options=[
                "No — works only for us",
                "Yes — has other clients / independent business",
                "Unknown / unclear",
            ],
        )
        benefits = st.selectbox(
            "Benefits offered (health, PTO, retirement)?" + REQ,
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
        help="Optional. Leave blank if nothing else to add.",
    )

    submitted = st.form_submit_button("Create classification analysis", type="primary")

if submitted:
    validate_required(
        {
            "Role / job title": role,
            "State where work will be performed": state,
        }
    )

    prompt = (
        f"Role: {role.strip()}.\n"
        f"State where work will be performed: {state}.\n"
        f"Hours: {hours}.\n"
        f"Duration: {duration}.\n"
        f"Equipment: {equipment}.\n"
        f"Payment structure: {payment}.\n"
        f"Other clients: {other_clients}.\n"
        f"Benefits offered: {benefits}.\n"
        f"Is role core to the business: {'Yes' if is_core else 'No'}.\n"
        f"Additional context: {extra.strip() or '(none)'}"
    )
    # If a company profile was loaded, fold the role details into it so the
    # agent gets both the company context and the classification request;
    # otherwise just send the role prompt as free text.
    agent_input = merge_company(profile, notes=prompt) if profile else prompt
    with st.spinner("Applying IRS + DOL + state tests..."):
        result = asyncio.run(run(agent_input))

    filename = f"classification-{role.strip().replace(' ', '-').lower()}.md"
    result_actions(markdown=result, filename=filename, position="top")
    st.markdown(result)
    st.divider()
    result_actions(markdown=result, filename=filename, position="bottom")
