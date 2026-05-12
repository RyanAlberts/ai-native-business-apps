# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Business Plan Implementation Manager."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import streamlit as st

from advanced_business_agents.multi_agent_apps.business_plan_implementation_manager.agent import run  # noqa


st.set_page_config(page_title="Business Plan Implementation Manager", page_icon="📋")
st.title("📋 Business Plan Implementation Manager")
st.caption(
    "A 4-stage pipeline: market research → SWOT → strategy → 30/60/90-day roadmap. "
    "Powered by `SequentialHarness`."
)

with st.form("inputs"):
    idea = st.text_area(
        "Business idea",
        height=80,
        placeholder="A vertical CRM for independent insurance brokers (2–10 employees).",
    )
    target = st.text_input("Target market (optional)", placeholder="US brokerages with 2–10 employees")
    founder_context = st.text_area(
        "Your background (optional)",
        height=60,
        placeholder="Former enterprise SaaS sales rep. 8 years experience selling to SMBs.",
    )
    budget = st.text_input("Budget / runway (optional)", placeholder="$50k savings, 6 months focused work")
    submitted = st.form_submit_button("Build the plan", type="primary")

if submitted and idea.strip():
    full_input = idea.strip()
    if target.strip():
        full_input += f"\n\nTarget market: {target.strip()}"
    if founder_context.strip():
        full_input += f"\n\nFounder background: {founder_context.strip()}"
    if budget.strip():
        full_input += f"\n\nBudget / runway: {budget.strip()}"

    progress = st.empty()
    stage_containers: dict[str, st.delta_generator.DeltaGenerator] = {}

    def on_stage(name: str, output: str) -> None:
        progress.info(f"Completed: {name}")
        with st.expander(f"📄 {name}", expanded=(name == "Implementation Roadmap")):
            st.markdown(output)

    with st.spinner("Running pipeline (this can take 1–3 minutes)..."):
        result = asyncio.run(run(full_input, on_stage_complete=on_stage))

    progress.success("All 4 stages complete.")
    combined = "\n\n---\n\n".join(f"# {name}\n\n{output}" for name, output in result.stages)
    st.download_button(
        "Download full plan as markdown",
        combined,
        file_name="business_plan.md",
    )
