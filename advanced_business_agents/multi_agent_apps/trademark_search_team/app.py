# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Trademark Search Team."""
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

from advanced_business_agents.multi_agent_apps.trademark_search_team.agent import run  # noqa


st.set_page_config(page_title="Trademark Search Team", page_icon="™️", layout="centered")

inject_styles()
sticky_header(
    emoji="™️",
    title="Trademark Search Team",
    caption=(
        "Federal TESS + state SoS + common-law + USPTO class identification — "
        "four research branches in parallel, then GO / CAUTION / NO-GO + TEAS pre-fill."
    ),
)

with st.form("trademark_form"):
    mark = st.text_input("Proposed mark" + REQ, placeholder="e.g. BLUEHORSE")
    goods = st.text_area(
        "Goods / services description" + REQ,
        placeholder=(
            "Describe what you'll sell under this mark. Example: "
            "'AI-powered photo editing software for mobile devices — "
            "downloadable iOS app + SaaS web product.'"
        ),
        height=100,
    )
    cols = st.columns(2)
    with cols[0]:
        state = st.text_input(
            "Founder's state of formation / primary operation" + REQ,
            value="CA",
            max_chars=2,
        ).upper()
    with cols[1]:
        in_use = st.radio(
            "Already using the mark in commerce?" + REQ,
            options=["No (intent-to-use)", "Yes (use-in-commerce)"],
        )
    notes = st.text_area(
        "Anything else relevant (geographic markets, related products, etc.)",
        placeholder="Optional",
        height=80,
        help="Optional. Leave blank if nothing else to add.",
    )
    submitted = st.form_submit_button(
        "Create trademark search report", type="primary"
    )

if submitted:
    validate_required(
        {
            "Proposed mark": mark,
            "Goods / services description": goods,
            "Founder's state of formation / primary operation": state,
        }
    )

    prompt = (
        f"Proposed mark: '{mark.strip()}'.\n"
        f"Goods/services: {goods.strip()}\n"
        f"Founder's state: {state}.\n"
        f"Use status: {in_use}.\n"
        f"Additional notes: {notes.strip() or '(none)'}"
    )

    progress_placeholders = {
        "Federal TESS": st.empty(),
        "State TM Registries": st.empty(),
        "Common-Law Scan": st.empty(),
        "Class ID": st.empty(),
        "Trademark Strategy Synthesis": st.empty(),
    }
    for name, slot in progress_placeholders.items():
        slot.info(f"⏳ {name} — pending")

    def on_stage(name: str, output: str) -> None:
        slot = progress_placeholders.get(name)
        if slot:
            slot.success(f"✅ {name} — complete ({len(output):,} chars)")

    with st.spinner(
        "Branches running in parallel — federal TESS, state registries, "
        "common-law scan, and class identification. Then synthesis. "
        "This takes 30-90 seconds."
    ):
        result = asyncio.run(run(prompt, on_stage_complete=on_stage))

    st.divider()
    st.markdown(result.final)

    with st.expander("📂 Raw branch findings (debug)"):
        for name, output in result.stages[:-1]:
            st.markdown(f"### {name}")
            st.markdown(output)
            st.markdown("---")

    filename = f"trademark-{mark.strip().replace(' ', '-').lower()}.md"
    st.divider()
    result_actions(markdown=result.final, filename=filename, position="bottom")
