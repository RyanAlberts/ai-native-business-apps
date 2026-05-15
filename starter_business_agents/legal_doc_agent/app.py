# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Legal Document Generator."""
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

from starter_business_agents.legal_doc_agent.agent import run  # noqa


DOC_TYPES = [
    UNSET,
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


st.set_page_config(page_title="Legal Document Generator", page_icon="📜", layout="centered")

inject_styles()
sticky_header(
    emoji="📜",
    title="Legal Document Generator",
    caption="Operating agreements, NDAs, IP assignments, ToS — templates for attorney review.",
)

with st.form("legal_doc_form"):
    doc_type = st.selectbox("Document type" + REQ, DOC_TYPES)
    business = st.text_input(
        "Your business (name + what it does)" + REQ,
        placeholder="Acme Labs LLC — software consultancy",
    )
    state = st.text_input("State of formation" + REQ, placeholder="Delaware")
    operating_state = st.text_input(
        "State(s) of operation" + REQ, placeholder="California"
    )

    col1, col2 = st.columns(2)
    with col1:
        party_a = st.text_input("Party A (your side)" + REQ, placeholder="Acme Labs LLC")
    with col2:
        party_b = st.text_input(
            "Party B (other side — leave blank for single-party docs)",
            placeholder="AcmeCorp Inc.",
            help="Optional. Many docs (Operating Agreement, ToS, Privacy Policy) have only one party.",
        )

    specifics = st.text_area(
        "Special terms or context" + REQ,
        placeholder=(
            "e.g. 2-year NDA term, governing law Delaware, no industry-specific "
            "triggers, this is for a sales conversation."
        ),
        height=120,
    )

    submitted = st.form_submit_button("Create document draft", type="primary")

if submitted:
    validate_required(
        {
            "Document type": doc_type,
            "Your business (name + what it does)": business,
            "State of formation": state,
            "State(s) of operation": operating_state,
            "Party A (your side)": party_a,
            "Special terms or context": specifics,
        }
    )

    full_input = (
        f"Document type: {doc_type}\n"
        f"Business: {business.strip()}\n"
        f"State of formation: {state.strip()}\n"
        f"State(s) of operation: {operating_state.strip()}\n"
        f"Party A: {party_a.strip()}\n"
        f"Party B: {party_b.strip() or '(not applicable)'}\n\n"
        f"Special terms / context: {specifics.strip()}"
    )
    safe_doc = doc_type.lower().replace(" ", "_").replace("/", "_")
    filename = f"{safe_doc}_draft.md"
    with st.spinner("Drafting..."):
        result = asyncio.run(run(full_input))

    result_actions(markdown=result, filename=filename, position="top")
    st.markdown(result)
    st.divider()
    result_actions(markdown=result, filename=filename, position="bottom")
