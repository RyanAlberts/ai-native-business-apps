# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Business Idea Validator template."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# Allow running with `streamlit run _template/app.py` from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from _template.agent import run


st.set_page_config(page_title="Business Idea Validator", page_icon="💡")
st.title("💡 Business Idea Validator")
st.caption("Get a fast, honest read on a startup idea — problem, MVP, risks, next step.")

idea = st.text_area(
    "Your business idea",
    placeholder="e.g. An AI-powered shopping list app for busy parents",
    height=120,
)

if st.button("Validate idea", type="primary") and idea.strip():
    with st.spinner("Thinking..."):
        result = asyncio.run(run(idea.strip()))
    st.markdown(result)
    st.download_button("Download as markdown", result, file_name="idea_validation.md")
