# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Incorporation Agent."""
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

from starter_business_agents.incorporation_agent.agent import run  # type: ignore  # noqa


st.set_page_config(page_title="Incorporation Agent", page_icon="🏛️", layout="centered")

inject_styles()
sticky_header(
    emoji="🏛️",
    title="Incorporation Agent",
    caption="Entity type, state of formation, registered agent, filing checklist.",
)

with st.form("incorporation_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Business name" + REQ, placeholder="Acme Bookkeeping")
        state = st.text_input("Founder's home state" + REQ, placeholder="Texas")
        cofounders = st.number_input(
            "Number of cofounders (including you)" + REQ,
            min_value=1,
            max_value=20,
            value=1,
        )
    with col2:
        funding = st.selectbox(
            "Funding plans" + REQ,
            [
                UNSET,
                "Bootstrap (no outside funding)",
                "SAFE / friends & family",
                "Priced seed round (9–18 months)",
                "Priced Series A+ (12–36 months)",
            ],
        )
        employees = st.selectbox(
            "Hiring plans (12 months)" + REQ,
            [UNSET, "Just founders", "1–5 employees", "6+ employees"],
        )

    description = st.text_area(
        "What does the business do? Any liability concerns?" + REQ,
        placeholder="e.g. SaaS for auto-body shops; we store customer financial records.",
        height=120,
    )

    submitted = st.form_submit_button("Create incorporation plan", type="primary")

if submitted:
    validate_required(
        {
            "Business name": name,
            "Founder's home state": state,
            "Funding plans": funding,
            "Hiring plans (12 months)": employees,
            "What does the business do?": description,
        }
    )

    full_input = (
        f"Business: {name.strip()}\n"
        f"Founder home state: {state.strip()}\n"
        f"Cofounders: {cofounders}\n"
        f"Funding plans: {funding}\n"
        f"Hiring plans (12 mo): {employees}\n\n"
        f"Description: {description.strip()}"
    )
    with st.spinner("Creating your incorporation plan..."):
        result = asyncio.run(run(full_input))

    result_actions(markdown=result, filename="incorporation_plan.md", position="top")
    st.markdown(result)
    st.divider()
    result_actions(markdown=result, filename="incorporation_plan.md", position="bottom")
