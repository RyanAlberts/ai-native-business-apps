# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Business Idea Validator template.

This file is the canonical reference for the agent-app UX contract.
Every agent app in this repo follows the same shape:

  1. inject_styles()                 # global stylesheet (once)
  2. sticky_header(emoji, title, caption)
  3. st.form(...) with REQ-marked inputs + UNSET sentinel selectboxes
  4. validate_required({...}) before running the agent
  5. result_actions(top) -> st.markdown(plan) -> result_actions(bottom)

See `core/ui.py` for the helpers used below.
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# Allow running with `streamlit run _template/app.py` from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from core.ui import (
    REQ,
    inject_styles,
    result_actions,
    sticky_header,
    validate_required,
)

from _template.agent import run


st.set_page_config(page_title="Business Idea Validator", page_icon="💡", layout="centered")

inject_styles()
sticky_header(
    emoji="💡",
    title="Business Idea Validator",
    caption="A fast, honest read on a startup idea — problem, MVP, risks, next step.",
)

with st.form("validator_form"):
    idea = st.text_area(
        "Your business idea" + REQ,
        placeholder="e.g. An AI-powered shopping list app for busy parents",
        height=120,
    )
    submitted = st.form_submit_button("Validate idea", type="primary")

if submitted:
    validate_required({"Your business idea": idea})

    with st.spinner("Thinking..."):
        result = asyncio.run(run(idea.strip()))

    result_actions(markdown=result, filename="idea_validation.md", position="top")
    st.markdown(result)
    st.divider()
    result_actions(markdown=result, filename="idea_validation.md", position="bottom")
