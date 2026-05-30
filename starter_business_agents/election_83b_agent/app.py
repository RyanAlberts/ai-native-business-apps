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

from core import merge_company
from core.ui import (
    REQ,
    company_loader,
    inject_styles,
    result_actions,
    sticky_header,
    validate_required,
)

from starter_business_agents.election_83b_agent.agent import run  # noqa


st.set_page_config(page_title="83(b) Election Agent", page_icon="📬", layout="centered")

inject_styles()
sticky_header(
    emoji="📬",
    title="83(b) Election Agent",
    caption=(
        "Prepare and time the IRS §83(b) election. 30-day deadline from grant. "
        "Free — what LegalZoom doesn't sell and Stripe Atlas bundles into $500 formation."
    ),
)

profile = company_loader(key="election_83b")

with st.form("election_83b_form"):
    st.markdown("### Your situation")
    cols = st.columns(2)
    with cols[0]:
        founder_name = st.text_input("Founder legal name" + REQ, placeholder="Jane Doe")
        founder_state = st.text_input(
            "State of residence (2-letter)" + REQ, value="CA", max_chars=2
        ).upper()
        founder_address = st.text_area(
            "Your mailing address" + REQ,
            placeholder="123 Main St\nAustin, TX 78701",
            height=80,
        )
    with cols[1]:
        issuer_name = st.text_input(
            "Issuer (company) name" + REQ,
            value=(profile.legal_name if profile else ""),
            placeholder="Acme Books Inc.",
        )
        issuer_state = st.text_input(
            "Issuer state of formation" + REQ,
            value=(profile.state_of_formation if profile else ""),
            placeholder="Delaware",
        )
        issuer_ein = st.text_input(
            "Issuer EIN",
            value=(profile.ein if profile else ""),
            placeholder="88-1234567",
            help="Optional. Leave blank if you don't have the EIN yet.",
        )

    st.markdown("### Stock grant")
    cols = st.columns(2)
    with cols[0]:
        grant_date = st.date_input(
            "Grant / transfer date" + REQ, value=dt.date.today(), format="YYYY-MM-DD"
        )
        share_count = st.number_input(
            "Number of shares" + REQ, min_value=1, value=8_000_000, step=1
        )
        share_class = st.text_input("Share class" + REQ, value="Common Stock")
    with cols[1]:
        fmv_per_share = st.number_input(
            "FMV per share at grant ($)" + REQ,
            min_value=0.0,
            value=0.0001,
            step=0.0001,
            format="%.4f",
        )
        price_per_share = st.number_input(
            "Price paid per share ($)" + REQ,
            min_value=0.0,
            value=0.0001,
            step=0.0001,
            format="%.4f",
        )

    restrictions = st.text_area(
        "Vesting + repurchase restrictions" + REQ,
        value=(
            "4-year monthly vesting with 1-year cliff. Company has the "
            "right to repurchase unvested shares at the price paid if "
            "founder leaves before vesting."
        ),
        height=80,
    )

    submitted = st.form_submit_button("Create 83(b) election", type="primary")


if submitted:
    validate_required(
        {
            "Founder legal name": founder_name,
            "State of residence": founder_state,
            "Your mailing address": founder_address,
            "Issuer (company) name": issuer_name,
            "Issuer state of formation": issuer_state,
            "Share class": share_class,
            "Vesting + repurchase restrictions": restrictions,
        }
    )

    prompt = (
        f"Founder: {founder_name.strip()}, residing at:\n{founder_address.strip()}\n"
        f"State of residence: {founder_state}.\n"
        f"Issuer: {issuer_name.strip()} (formed in {issuer_state.strip()}, "
        f"EIN {issuer_ein.strip() or 'N/A'}).\n"
        f"Granted {share_count:,} shares of {share_class.strip()} on "
        f"{grant_date.isoformat()}. FMV at grant: ${fmv_per_share:.4f}/share. "
        f"Price paid: ${price_per_share:.4f}/share.\n"
        f"Restrictions: {restrictions.strip()}\n"
        "I have not yet filled in my TIN/SSN — leave a placeholder for me."
    )
    agent_input = merge_company(profile, notes=prompt) if profile else prompt
    with st.spinner("Preparing your 83(b) election letter and mailing kit..."):
        result = asyncio.run(run(agent_input))

    filename = f"83b-election-{grant_date.isoformat()}.md"
    result_actions(markdown=result, filename=filename, position="top")
    st.markdown(result)
    st.divider()
    result_actions(markdown=result, filename=filename, position="bottom")
