# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Website Launch Team."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import streamlit as st

from core.ui import (
    REQ,
    inject_styles,
    result_actions,
    sticky_header,
    validate_required,
)

from advanced_business_agents.multi_agent_apps.website_launch_team.agent import run  # noqa


st.set_page_config(page_title="Website Launch Team", page_icon="🌐", layout="centered")

inject_styles()
sticky_header(
    emoji="🌐",
    title="Website Launch Team",
    caption="Brand → Architecture → Copy → Launch checklist. Ship a site in 2 weeks.",
)

with st.form("website_launch_form"):
    business = st.text_area(
        "Business description" + REQ,
        height=80,
        placeholder="AI-powered hiring screener for SaaS recruiting teams.",
    )
    audience = st.text_input(
        "Target audience" + REQ,
        placeholder="Talent acquisition leads at 50–500 person SaaS companies",
    )
    background = st.text_area(
        "Founder background" + REQ,
        height=60,
        placeholder="Former recruiter turned engineer; 6 years in talent",
    )
    budget = st.text_input(
        "Budget + timeline" + REQ,
        placeholder="$30k for site + initial marketing; live in 14 days",
    )
    submitted = st.form_submit_button("Create the launch plan", type="primary")

if submitted:
    validate_required(
        {
            "Business description": business,
            "Target audience": audience,
            "Founder background": background,
            "Budget + timeline": budget,
        }
    )

    full_input = (
        business.strip()
        + f"\n\nTarget audience: {audience.strip()}"
        + f"\n\nFounder background: {background.strip()}"
        + f"\n\nBudget / timeline: {budget.strip()}"
    )

    progress = st.empty()

    def on_stage(name: str, output: str) -> None:
        progress.info(f"Completed: {name}")
        expanded = name == "Launch Checklist"
        with st.expander(f"🌐 {name}", expanded=expanded):
            st.markdown(output)

    with st.spinner("Running 4-stage pipeline (this can take 1–3 minutes)..."):
        result = asyncio.run(run(full_input, on_stage_complete=on_stage))

    progress.success("All 4 stages complete.")
    combined = "\n\n---\n\n".join(
        f"# {name}\n\n{output}" for name, output in result.stages
    )

    st.divider()
    result_actions(
        markdown=combined, filename="website_launch_plan.md", position="bottom"
    )
