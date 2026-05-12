# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Legal Document Generator."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from starter_business_agents.legal_doc_agent.agent import run  # noqa


DOC_TYPES = [
    "Operating Agreement (single-member LLC)",
    "Operating Agreement (multi-member LLC)",
    "Mutual NDA",
    "Unilateral NDA",
    "IP Assignment Agreement",
    "Independent Contractor Agreement",
    "Terms of Service (web/SaaS)",
    "Privacy Policy (web/SaaS)",
    "Service Agreement / SOW",
    "Cofounder Agreement",
]


st.set_page_config(page_title="Legal Document Generator", page_icon="📜")
st.title("📜 Legal Document Generator")
st.caption(
    "Draft operating agreements, NDAs, IP assignments, ToS, and more. "
    "Templates only — get attorney review before signing."
)

doc_type = st.selectbox("Document type", DOC_TYPES, index=2)
business = st.text_input(
    "Your business (name + what it does)",
    placeholder="Acme Labs LLC — software consultancy",
)
state = st.text_input("State of formation", placeholder="Delaware")
operating_state = st.text_input("State(s) of operation", placeholder="California")

col1, col2 = st.columns(2)
with col1:
    party_a = st.text_input("Party A (your side)", placeholder="Acme Labs LLC")
with col2:
    party_b = st.text_input(
        "Party B (other side, if applicable)",
        placeholder="AcmeCorp Inc.",
    )

specifics = st.text_area(
    "Special terms or context",
    placeholder=(
        "e.g. 2-year NDA term, governing law Delaware, no industry-specific "
        "triggers, this is for a sales conversation."
    ),
    height=120,
)

if st.button("Draft document", type="primary") and business.strip():
    full_input = (
        f"Document type: {doc_type}\n"
        f"Business: {business}\n"
        f"State of formation: {state or '(not specified)'}\n"
        f"State(s) of operation: {operating_state or '(not specified)'}\n"
        f"Party A: {party_a or '(not specified)'}\n"
        f"Party B: {party_b or '(not applicable)'}\n\n"
        f"Special terms / context: {specifics.strip() or '(none provided)'}"
    )
    with st.spinner("Drafting..."):
        result = asyncio.run(run(full_input))
    st.markdown(result)
    st.download_button(
        "Download as markdown",
        result,
        file_name=f"{doc_type.lower().replace(' ', '_').replace('/', '_')}_draft.md",
    )
