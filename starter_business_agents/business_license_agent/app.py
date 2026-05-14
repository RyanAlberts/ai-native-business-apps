# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Business License + DBA Agent."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from starter_business_agents.business_license_agent.agent import run


st.set_page_config(page_title="Business License + DBA Agent", page_icon="📋")
st.title("📋 Business License + DBA Agent")
st.caption(
    "Every license, permit, and DBA registration you need at the federal / "
    "state / county / city level — for your specific industry, city, and "
    "state. Replaces $99–$300/location 'business license services'. $0."
)

with st.form("inputs"):
    cols = st.columns(2)
    with cols[0]:
        entity_name = st.text_input(
            "Registered entity name",
            placeholder="e.g. Mission Coffee LLC",
        )
        operating_name = st.text_input(
            "Name you'll operate under (if different — triggers DBA)",
            placeholder="e.g. The Daily Grind (or leave blank if same as entity)",
        )
        industry = st.text_input(
            "Industry / what the business does",
            placeholder="e.g. specialty coffee shop with kitchen + on-premise seating",
        )
    with cols[1]:
        state = st.text_input(
            "State of operation (2-letter)",
            value="CA",
            max_chars=2,
        ).upper()
        city = st.text_input(
            "City",
            placeholder="e.g. San Francisco",
        )
        county = st.text_input(
            "County",
            placeholder="e.g. San Francisco County",
        )

    employees = st.number_input(
        "Number of employees (Year 1)",
        min_value=0,
        value=2,
        step=1,
    )
    physical_premises = st.checkbox(
        "Has a physical premises (storefront / office / kitchen)?",
        value=True,
    )
    home_based = st.checkbox(
        "Operating from home (residential zone)?",
        value=False,
    )
    sells_goods = st.checkbox(
        "Sells tangible goods (triggers sales tax permit)?",
        value=True,
    )
    industry_extras = st.multiselect(
        "Industry-specific triggers (select all that apply)",
        options=[
            "Food service / prepared food",
            "Alcohol / beer / wine",
            "Contractor / construction",
            "Cosmetology / barbering",
            "Professional services (CPA / Atty / Real Estate / Medical)",
            "Childcare / eldercare",
            "Cannabis (where legal)",
            "Live entertainment / music",
            "Outdoor seating / parklet",
            "Sign on building exterior",
        ],
    )
    submitted = st.form_submit_button(
        "Generate license + permit checklist", type="primary"
    )

if submitted:
    if not entity_name or not industry or not state or not city:
        st.error("Entity name, industry, state, and city are all required.")
    else:
        dba_clause = (
            f"Operating name (DBA): {operating_name}."
            if operating_name and operating_name != entity_name
            else "Operating under exact registered entity name (no DBA needed)."
        )
        triggers = ", ".join(industry_extras) if industry_extras else "(none specified)"
        prompt = (
            f"Registered entity: {entity_name}\n"
            f"{dba_clause}\n"
            f"Industry: {industry}\n"
            f"Location: {city}, {county or '(no county given)'}, {state}\n"
            f"Employees year 1: {employees}\n"
            f"Has physical premises: {'Yes' if physical_premises else 'No'}\n"
            f"Operating from home: {'Yes' if home_based else 'No'}\n"
            f"Sells tangible goods: {'Yes' if sells_goods else 'No'}\n"
            f"Industry-specific triggers: {triggers}"
        )
        with st.spinner(
            "Identifying licenses + permits across federal / state / "
            "county / city. Using WebSearch for city- and county-specific "
            "requirements — 30-60 seconds."
        ):
            result = asyncio.run(run(prompt))
        st.markdown(result)
        st.download_button(
            "Download checklist (markdown)",
            result,
            file_name=f"license-checklist-{city.replace(' ', '-')}.md",
        )
