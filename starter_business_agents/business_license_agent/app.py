# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Business License + DBA Agent."""
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

from starter_business_agents.business_license_agent.agent import run  # noqa


st.set_page_config(
    page_title="Business License + DBA Agent", page_icon="📋", layout="centered"
)

inject_styles()
sticky_header(
    emoji="📋",
    title="Business License + DBA Agent",
    caption=(
        "Every license, permit, and DBA registration you need at the federal / "
        "state / county / city level. Replaces $99–$300/location services."
    ),
)

profile = company_loader(key="business_license")

with st.form("license_form"):
    cols = st.columns(2)
    with cols[0]:
        entity_name = st.text_input(
            "Registered entity name" + REQ,
            placeholder="e.g. Mission Coffee LLC",
        )
        operating_name = st.text_input(
            "Name you'll operate under (leave blank if same as entity — otherwise triggers DBA)",
            placeholder="e.g. The Daily Grind",
            help="Optional. Only fill in if you'll operate under a different name than the registered entity.",
        )
        industry = st.text_input(
            "Industry / what the business does" + REQ,
            placeholder="e.g. specialty coffee shop with kitchen + on-premise seating",
        )
    with cols[1]:
        state = st.text_input(
            "State of operation (2-letter)" + REQ,
            value="CA",
            max_chars=2,
        ).upper()
        city = st.text_input(
            "City" + REQ,
            placeholder="e.g. San Francisco",
        )
        county = st.text_input(
            "County" + REQ,
            placeholder="e.g. San Francisco County",
        )

    employees = st.number_input(
        "Number of employees (Year 1)" + REQ,
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
        help="Optional. Pick zero or more — leave empty if none apply.",
    )
    submitted = st.form_submit_button(
        "Create license + permit checklist", type="primary"
    )

if submitted:
    validate_required(
        {
            "Registered entity name": entity_name,
            "Industry / what the business does": industry,
            "State of operation": state,
            "City": city,
            "County": county,
        }
    )

    dba_clause = (
        f"Operating name (DBA): {operating_name.strip()}."
        if operating_name.strip() and operating_name.strip() != entity_name.strip()
        else "Operating under exact registered entity name (no DBA needed)."
    )
    triggers = ", ".join(industry_extras) if industry_extras else "(none specified)"
    prompt = (
        f"Registered entity: {entity_name.strip()}\n"
        f"{dba_clause}\n"
        f"Industry: {industry.strip()}\n"
        f"Location: {city.strip()}, {county.strip()}, {state}\n"
        f"Employees year 1: {employees}\n"
        f"Has physical premises: {'Yes' if physical_premises else 'No'}\n"
        f"Operating from home: {'Yes' if home_based else 'No'}\n"
        f"Sells tangible goods: {'Yes' if sells_goods else 'No'}\n"
        f"Industry-specific triggers: {triggers}"
    )
    # Fold the form into a loaded profile (if any) so the agent has company
    # context too; otherwise send the licensing prompt as free text.
    agent_input = merge_company(profile, notes=prompt) if profile else prompt
    with st.spinner(
        "Identifying licenses + permits across federal / state / county / "
        "city. Using WebSearch for city- and county-specific requirements — "
        "30-60 seconds."
    ):
        result = asyncio.run(run(agent_input))

    filename = f"license-checklist-{city.strip().replace(' ', '-').lower()}.md"
    result_actions(markdown=result, filename=filename, position="top")
    st.markdown(result)
    st.divider()
    result_actions(markdown=result, filename=filename, position="bottom")
