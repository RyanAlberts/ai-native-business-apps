# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Founding Journey — the unified Day-0 back office."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import streamlit as st

from core import Company, Founder
from core.brand import NAME
from core.ui import (
    REQ,
    UNSET,
    artifact_downloads,
    inject_styles,
    result_actions,
    sticky_header,
    validate_required,
)

from advanced_business_agents.multi_agent_apps.founding_journey.agent import run  # type: ignore  # noqa


st.set_page_config(page_title="Founding Journey", page_icon="🚀", layout="centered")

inject_styles()
sticky_header(
    emoji="🚀",
    title=f"{NAME} · Founding Journey",
    caption="Fill in your company once — get a complete Day-0 Formation Packet: "
    "incorporation, 83(b), legal docs, banking, and a compliance calendar.",
)

with st.form("journey_form"):
    col1, col2 = st.columns(2)
    with col1:
        legal_name = st.text_input("Company name" + REQ, placeholder="Northwind Robotics, Inc.")
        home_state = st.text_input("Founders' home state" + REQ, placeholder="California")
        state_of_formation = st.text_input(
            "State of formation (blank = let the agent choose)",
            placeholder="Delaware",
        )
        industry = st.text_input("Industry", placeholder="Robotics / hardware")
    with col2:
        entity_type = st.selectbox(
            "Preferred entity type (blank = let the agent choose)",
            [UNSET, "C-Corp", "S-Corp", "LLC", "Not sure — recommend one"],
        )
        funding_stage = st.selectbox(
            "Funding plans" + REQ,
            [
                UNSET,
                "Bootstrap (no outside funding)",
                "SAFE / friends & family",
                "Priced seed round (9–18 months)",
                "Priced Series A+ (12–36 months)",
            ],
        )
        employees_plan = st.selectbox(
            "Hiring plans (12 months)" + REQ,
            [UNSET, "Just founders", "1–5 employees", "6+ employees"],
        )
        num_founders = st.number_input(
            "Number of founders" + REQ, min_value=1, max_value=20, value=1
        )

    one_liner = st.text_area(
        "What does the business do? Any liability concerns?" + REQ,
        placeholder="Warehouse picking robots sold to mid-size 3PLs; hardware lives in "
        "customer warehouses, so we have product-liability exposure.",
        height=110,
    )
    formation_date = st.text_input(
        "Stock issuance / formation date (YYYY-MM-DD, optional — enables the 83(b) "
        "and franchise-tax calendar)",
        placeholder="2026-06-01",
    )

    submitted = st.form_submit_button("Run the founding journey →", type="primary")

if submitted:
    validate_required(
        {
            "Company name": legal_name,
            "Founders' home state": home_state,
            "Funding plans": funding_stage,
            "Hiring plans (12 months)": employees_plan,
            "What does the business do?": one_liner,
        }
    )

    company = Company(
        legal_name=legal_name.strip(),
        one_liner=one_liner.strip(),
        industry=industry.strip(),
        home_state=home_state.strip(),
        state_of_formation=state_of_formation.strip(),
        entity_type="" if entity_type in (UNSET, "Not sure — recommend one") else entity_type,
        funding_stage=funding_stage,
        employees_plan=employees_plan,
        formation_date=formation_date.strip(),
        liability_notes=one_liner.strip(),
        founders=[Founder(name=f"Founder {i+1}") for i in range(int(num_founders))],
    )

    progress = st.progress(0.0, text="Starting the founding journey…")
    status = st.status("Running specialists…", expanded=True)
    # 5 specialist steps + 1 synthesis.
    total = 6
    done = {"n": 0}

    async def _on_step(step):
        done["n"] += 1
        ok = getattr(step, "ok", True)
        icon = "✅" if ok else "⚠️"
        label = f"{step.emoji} {step.title}" + ("" if ok else " — skipped (see packet)")
        progress.progress(done["n"] / total, text=f"{icon} {step.emoji} {step.title}")
        status.write(f"{icon} {label}")

    with st.spinner("This runs five agents in sequence — give it a minute…"):
        result = asyncio.run(run(company, on_step=_on_step))
    progress.progress(1.0, text="Day-0 Formation Packet ready.")
    status.update(label="Journey complete", state="complete", expanded=False)

    # If any specialist degraded, tell the founder up front rather than
    # letting them assume the packet is complete.
    if result.failed_steps:
        names = ", ".join(f"{s.emoji} {s.title}" for s in result.failed_steps)
        st.warning(
            f"{len(result.failed_steps)} step(s) couldn't complete automatically: "
            f"{names}. The packet below covers everything that did run — "
            "re-run the journey or run those agents individually to fill the gaps."
        )

    artifacts = result.artifacts()

    st.divider()
    result_actions(markdown=result.packet_markdown, filename="formation-packet.md", position="top")
    st.subheader("⬇️ Prepare-to-submit artifacts")
    artifact_downloads(artifacts, position="top")
    st.divider()

    st.markdown(result.packet_markdown)

    with st.expander("See each specialist's full output"):
        for step in result.steps:
            flag = "" if getattr(step, "ok", True) else " ⚠️ (skipped — failed)"
            st.markdown(f"### {step.emoji} {step.title}{flag}")
            st.markdown(step.output)
            st.divider()

    result_actions(markdown=result.packet_markdown, filename="formation-packet.md", position="bottom")
    artifact_downloads(artifacts, position="bottom")
