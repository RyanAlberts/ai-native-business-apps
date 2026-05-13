# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the 83(b) Election Agent."""
from __future__ import annotations

import asyncio
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from starter_business_agents.election_83b_agent.agent import run


st.set_page_config(page_title="83(b) Election Agent", page_icon="📬")
st.title("📬 83(b) Election Agent")
st.caption(
    "Prepare and time the IRS §83(b) election. 30-day deadline from your "
    "grant date. Free + open source — what LegalZoom doesn't sell and "
    "Stripe Atlas bundles into their $500 formation."
)

with st.form("inputs"):
    st.markdown("### Your situation")
    cols = st.columns(2)
    with cols[0]:
        founder_name = st.text_input("Founder legal name", placeholder="Jane Doe")
        founder_state = st.text_input(
            "State of residence (2-letter)", value="CA", max_chars=2
        ).upper()
        founder_address = st.text_area(
            "Your mailing address",
            placeholder="123 Main St\nAustin, TX 78701",
            height=80,
        )
    with cols[1]:
        issuer_name = st.text_input(
            "Issuer (company) name", placeholder="Acme Books Inc."
        )
        issuer_state = st.text_input(
            "Issuer state of formation", placeholder="Delaware"
        )
        issuer_ein = st.text_input(
            "Issuer EIN (optional)", placeholder="88-1234567"
        )

    st.markdown("### Stock grant")
    cols = st.columns(2)
    with cols[0]:
        grant_date = st.date_input(
            "Grant / transfer date", value=dt.date.today(), format="YYYY-MM-DD"
        )
        share_count = st.number_input(
            "Number of shares", min_value=1, value=8_000_000, step=1
        )
        share_class = st.text_input("Share class", value="Common Stock")
    with cols[1]:
        fmv_per_share = st.number_input(
            "FMV per share at grant ($)",
            min_value=0.0,
            value=0.0001,
            step=0.0001,
            format="%.4f",
        )
        price_per_share = st.number_input(
            "Price paid per share ($)",
            min_value=0.0,
            value=0.0001,
            step=0.0001,
            format="%.4f",
        )

    restrictions = st.text_area(
        "Vesting + repurchase restrictions",
        value=(
            "4-year monthly vesting with 1-year cliff. Company has the "
            "right to repurchase unvested shares at the price paid if "
            "founder leaves before vesting."
        ),
        height=80,
    )

    submitted = st.form_submit_button("Prepare 83(b) election", type="primary")


if submitted:
    if not founder_name or not founder_address or not issuer_name:
        st.error("Founder name, address, and issuer name are required.")
    else:
        prompt = (
            f"Founder: {founder_name}, residing at:\n{founder_address}\n"
            f"State of residence: {founder_state}.\n"
            f"Issuer: {issuer_name} (formed in {issuer_state}, EIN {issuer_ein or 'N/A'}).\n"
            f"Granted {share_count:,} shares of {share_class} on "
            f"{grant_date.isoformat()}. FMV at grant: ${fmv_per_share:.4f}/share. "
            f"Price paid: ${price_per_share:.4f}/share.\n"
            f"Restrictions: {restrictions}\n"
            "I have not yet filled in my TIN/SSN — leave a placeholder for me."
        )
        with st.spinner("Preparing your 83(b) election letter and mailing kit..."):
            result = asyncio.run(run(prompt))
        st.markdown(result)
        st.download_button(
            "Download full output (markdown)",
            result,
            file_name=f"83b-election-{grant_date.isoformat()}.md",
        )
