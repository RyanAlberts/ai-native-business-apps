# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Business Plan Implementation Manager."""
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

from advanced_business_agents.multi_agent_apps.business_plan_implementation_manager.agent import run  # noqa


st.set_page_config(
    page_title="Business Plan Implementation Manager",
    page_icon="📋",
    layout="centered",
)

inject_styles()
sticky_header(
    emoji="📋",
    title="Business Plan Implementation Manager",
    caption="4-stage pipeline: market research → SWOT → strategy → 30/60/90-day roadmap.",
)

with st.form("business_plan_form"):
    idea = st.text_area(
        "Business idea" + REQ,
        height=80,
        placeholder="A vertical CRM for independent insurance brokers (2–10 employees).",
    )
    target = st.text_input(
        "Target market" + REQ,
        placeholder="US brokerages with 2–10 employees",
    )
    founder_context = st.text_area(
        "Your background" + REQ,
        height=60,
        placeholder="Former enterprise SaaS sales rep. 8 years selling to SMBs.",
    )
    budget = st.text_input(
        "Budget / runway" + REQ,
        placeholder="$50k savings, 6 months focused work",
    )
    submitted = st.form_submit_button("Create the plan", type="primary")

if submitted:
    validate_required(
        {
            "Business idea": idea,
            "Target market": target,
            "Your background": founder_context,
            "Budget / runway": budget,
        }
    )

    full_input = (
        idea.strip()
        + f"\n\nTarget market: {target.strip()}"
        + f"\n\nFounder background: {founder_context.strip()}"
        + f"\n\nBudget / runway: {budget.strip()}"
    )

    progress = st.empty()

    def on_stage(name: str, output: str) -> None:
        progress.info(f"Completed: {name}")
        with st.expander(f"📄 {name}", expanded=(name == "Implementation Roadmap")):
            st.markdown(output)

    with st.spinner("Running 4-stage pipeline (this can take 1–3 minutes)..."):
        result = asyncio.run(run(full_input, on_stage_complete=on_stage))

    progress.success("All 4 stages complete.")
    combined = "\n\n---\n\n".join(
        f"# {name}\n\n{output}" for name, output in result.stages
    )

    st.divider()
    result_actions(markdown=combined, filename="business_plan.md", position="bottom")
