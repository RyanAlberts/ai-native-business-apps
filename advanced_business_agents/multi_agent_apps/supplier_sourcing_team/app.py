# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Supplier Sourcing Team."""
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

from advanced_business_agents.multi_agent_apps.supplier_sourcing_team.agent import run  # noqa


st.set_page_config(page_title="Supplier Sourcing Team", page_icon="🏭", layout="centered")

inject_styles()
sticky_header(
    emoji="🏭",
    title="Supplier Sourcing Team",
    caption="Source → Vet → RFP → Compare. From 'I need this made' to a ready-to-send RFP.",
)

with st.form("supplier_sourcing_form"):
    item = st.text_area(
        "What are you sourcing?" + REQ,
        height=80,
        placeholder="Contract-manufactured silicone kitchenware (DTC brand)",
    )
    volume = st.text_input(
        "Volume (initial + projected)" + REQ,
        placeholder="5,000 units across 3 SKUs; 50,000 units yr 1",
    )
    budget = st.text_input(
        "Budget per unit (landed)" + REQ,
        placeholder="$4/unit landed",
    )
    quality = st.text_input(
        "Quality / certification bar" + REQ,
        placeholder="FDA food-safe certified",
    )
    timeline = st.text_input(
        "Timeline" + REQ,
        placeholder="Samples in 6 wks, production order in 10 wks",
    )
    geography = st.text_input(
        "Geographic openness" + REQ,
        placeholder="US, Mexico, or Asia",
    )
    submitted = st.form_submit_button("Create sourcing plan", type="primary")

if submitted:
    validate_required(
        {
            "What are you sourcing?": item,
            "Volume (initial + projected)": volume,
            "Budget per unit (landed)": budget,
            "Quality / certification bar": quality,
            "Timeline": timeline,
            "Geographic openness": geography,
        }
    )

    full_input = (
        f"Need: {item.strip()}\n"
        f"Volume: {volume.strip()}\n"
        f"Budget: {budget.strip()}\n"
        f"Quality: {quality.strip()}\n"
        f"Timeline: {timeline.strip()}\n"
        f"Geography: {geography.strip()}"
    )

    progress = st.empty()

    def on_stage(name: str, output: str) -> None:
        progress.info(f"Completed: {name}")
        expanded = name == "Comparison Matrix"
        with st.expander(f"🏭 {name}", expanded=expanded):
            st.markdown(output)

    with st.spinner("Running 4-stage pipeline (this can take 1–3 minutes)..."):
        result = asyncio.run(run(full_input, on_stage_complete=on_stage))

    progress.success("All 4 stages complete.")
    combined = "\n\n---\n\n".join(
        f"# {name}\n\n{output}" for name, output in result.stages
    )

    st.divider()
    result_actions(
        markdown=combined, filename="supplier_sourcing_plan.md", position="bottom"
    )
