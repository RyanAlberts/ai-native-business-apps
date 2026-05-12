# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Incorporation Agent."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from starter_business_agents.incorporation_agent.agent import run  # type: ignore  # noqa


st.set_page_config(page_title="Incorporation Agent", page_icon="🏛️")
st.title("🏛️ Incorporation Agent")
st.caption(
    "Tell me about your business and I'll recommend an entity type, "
    "state of formation, and a filing checklist."
)

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Business name (optional)", placeholder="Acme Bookkeeping")
    state = st.text_input("Founder's home state", placeholder="Texas")
    cofounders = st.number_input("Number of cofounders (including you)", min_value=1, max_value=20, value=1)
with col2:
    funding = st.selectbox(
        "Funding plans",
        ["Bootstrap (no outside funding)", "SAFE / friends & family", "Priced seed round (9–18 months)", "Priced Series A+ (12–36 months)"],
    )
    employees = st.selectbox(
        "Hiring plans (12 months)",
        ["Just founders", "1–5 employees", "6+ employees"],
    )

description = st.text_area(
    "What does the business do? Any liability concerns?",
    placeholder="e.g. SaaS for auto-body shops; we store customer financial records.",
    height=120,
)

if st.button("Recommend incorporation plan", type="primary") and description.strip():
    full_input = (
        f"Business: {name or '(unnamed)'}\n"
        f"Founder home state: {state or '(not specified)'}\n"
        f"Cofounders: {cofounders}\n"
        f"Funding plans: {funding}\n"
        f"Hiring plans (12 mo): {employees}\n\n"
        f"Description: {description.strip()}"
    )
    with st.spinner("Drafting incorporation plan..."):
        result = asyncio.run(run(full_input))
    st.markdown(result)
    st.download_button(
        "Download as markdown",
        result,
        file_name="incorporation_plan.md",
    )
