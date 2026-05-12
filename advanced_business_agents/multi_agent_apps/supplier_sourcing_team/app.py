# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Supplier Sourcing Team."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import streamlit as st

from advanced_business_agents.multi_agent_apps.supplier_sourcing_team.agent import run  # noqa


st.set_page_config(page_title="Supplier Sourcing Team", page_icon="🏭")
st.title("🏭 Supplier Sourcing Team")
st.caption(
    "Source → Vet → RFP → Compare. A 4-stage pipeline that takes you from "
    "'I need this made' to a ready-to-send RFP and a comparison matrix."
)

with st.form("inputs"):
    item = st.text_area(
        "What are you sourcing?",
        height=80,
        placeholder="Contract-manufactured silicone kitchenware (DTC brand)",
    )
    volume = st.text_input(
        "Volume (initial + projected)",
        placeholder="5,000 units across 3 SKUs; 50,000 units yr 1",
    )
    budget = st.text_input(
        "Budget per unit (landed)",
        placeholder="$4/unit landed",
    )
    quality = st.text_input(
        "Quality / certification bar",
        placeholder="FDA food-safe certified",
    )
    timeline = st.text_input(
        "Timeline",
        placeholder="Samples in 6 wks, production order in 10 wks",
    )
    geography = st.text_input(
        "Geographic openness",
        placeholder="US, Mexico, or Asia",
    )
    submitted = st.form_submit_button("Run sourcing pipeline", type="primary")

if submitted and item.strip():
    full_input = f"Need: {item.strip()}"
    if volume.strip():
        full_input += f"\nVolume: {volume.strip()}"
    if budget.strip():
        full_input += f"\nBudget: {budget.strip()}"
    if quality.strip():
        full_input += f"\nQuality: {quality.strip()}"
    if timeline.strip():
        full_input += f"\nTimeline: {timeline.strip()}"
    if geography.strip():
        full_input += f"\nGeography: {geography.strip()}"

    progress = st.empty()

    def on_stage(name: str, output: str) -> None:
        progress.info(f"Completed: {name}")
        expanded = name == "Comparison Matrix"
        with st.expander(f"🏭 {name}", expanded=expanded):
            st.markdown(output)

    with st.spinner("Running 4 stages (this can take 1–3 minutes)..."):
        result = asyncio.run(run(full_input, on_stage_complete=on_stage))

    progress.success("All 4 stages complete.")
    combined = "\n\n---\n\n".join(f"# {name}\n\n{output}" for name, output in result.stages)
    st.download_button(
        "Download full plan as markdown",
        combined,
        file_name="supplier_sourcing_plan.md",
    )
