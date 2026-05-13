# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Trademark Search Team."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import streamlit as st

from advanced_business_agents.multi_agent_apps.trademark_search_team.agent import run


st.set_page_config(page_title="Trademark Search Team", page_icon="™️")
st.title("™️ Trademark Search Team")
st.caption(
    "Federal TESS + state SoS + common-law + USPTO class identification — "
    "four research branches run in parallel, then a synthesis agent gives "
    "you the GO / CAUTION / NO-GO verdict + TEAS application pre-fill + "
    "fee estimate. Replaces LegalZoom's $199–$899 trademark services. $0."
)

with st.form("inputs"):
    mark = st.text_input(
        "Proposed mark",
        placeholder="e.g. BLUEHORSE",
    )
    goods = st.text_area(
        "Goods / services description",
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
            "Founder's state of formation / primary operation",
            value="CA",
            max_chars=2,
        ).upper()
    with cols[1]:
        in_use = st.radio(
            "Already using the mark in commerce?",
            options=["No (intent-to-use)", "Yes (use-in-commerce)"],
        )
    notes = st.text_area(
        "Anything else relevant (geographic markets, related products, etc.)",
        placeholder="(optional)",
        height=80,
    )
    submitted = st.form_submit_button(
        "Run trademark search (4 branches in parallel)", type="primary"
    )

if submitted:
    if not mark or not goods:
        st.error("Mark and goods/services description are both required.")
    else:
        prompt = (
            f"Proposed mark: '{mark}'.\n"
            f"Goods/services: {goods}\n"
            f"Founder's state: {state}.\n"
            f"Use status: {in_use}.\n"
            f"Additional notes: {notes or '(none)'}"
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

        def on_stage(name, output):
            slot = progress_placeholders.get(name)
            if slot:
                slot.success(f"✅ {name} — complete ({len(output):,} chars)")

        with st.spinner(
            "Branches running in parallel — federal TESS, state registries, "
            "common-law scan, and class identification. Then synthesis. "
            "This takes 30-90 seconds."
        ):
            result = asyncio.run(run(prompt, on_stage_complete=on_stage))

        st.markdown("---")
        st.markdown(result.final)

        with st.expander("📂 Raw branch findings (debug)"):
            for name, output in result.stages[:-1]:
                st.markdown(f"### {name}")
                st.markdown(output)
                st.markdown("---")

        st.download_button(
            "Download final report (markdown)",
            result.final,
            file_name=f"trademark-{mark.replace(' ', '-')}.md",
        )
