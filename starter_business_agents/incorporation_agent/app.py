# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Streamlit UI for the Incorporation Agent."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st
import streamlit.components.v1 as components

from starter_business_agents.incorporation_agent.agent import run  # type: ignore  # noqa


# Sentinel placeholder for "user hasn't chosen yet" in selectboxes.
_UNSET = "— select one —"

# Required-field marker rendered next to every label.
_REQ = " :red[*]"


st.set_page_config(page_title="Incorporation Agent", page_icon="🏛️", layout="centered")


# ── Sticky header + print styling ──────────────────────────────────────
# The header below uses position:sticky so it pins to the top of the
# viewport as the user scrolls. The @media print block hides interactive
# chrome (form, buttons, sticky styling) so Cmd-P / the print button
# produce a clean export of just the plan content.
st.markdown(
    """
<style>
/* Sticky header — theme-aware. Defaults to light; flips on dark mode
   via prefers-color-scheme. Translucent + backdrop-filter so content
   scrolling underneath is hinted at, but text stays readable. */
.incorp-sticky {
    position: sticky;
    top: 0;
    z-index: 100;
    padding: 0.75rem 0 0.5rem 0;
    margin: -1rem 0 1.25rem 0;
    border-bottom: 1px solid rgba(128, 128, 128, 0.25);
    background: rgba(255, 255, 255, 0.92);
    color: rgb(38, 39, 48);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}
.incorp-sticky h1 {
    margin: 0 0 0.25rem 0;
    font-size: 1.6rem;
    color: inherit;
}
.incorp-sticky p {
    margin: 0;
    font-size: 0.9rem;
    opacity: 0.85;
    color: inherit;
}

/* Dark mode — Streamlit's default dark background is rgb(14, 17, 23). */
@media (prefers-color-scheme: dark) {
    .incorp-sticky {
        background: rgba(14, 17, 23, 0.92);
        color: rgb(250, 250, 250);
        border-bottom-color: rgba(255, 255, 255, 0.12);
    }
}

/* Belt-and-suspenders: also pick up Streamlit's explicit theme attr if
   the user toggled theme in Settings (overrides OS-level pref). */
[data-theme="dark"] .incorp-sticky,
.stApp[data-theme="dark"] .incorp-sticky {
    background: rgba(14, 17, 23, 0.92);
    color: rgb(250, 250, 250);
    border-bottom-color: rgba(255, 255, 255, 0.12);
}

@media print {
    .incorp-sticky { position: static !important; border: none !important; margin: 0 0 1rem 0 !important; padding: 0 !important; background: transparent !important; color: black !important; backdrop-filter: none !important; }
    .stForm, [data-testid="stFormSubmitButton"], .print-row { display: none !important; }
    .stDownloadButton { display: none !important; }
    header[data-testid="stHeader"], footer, [data-testid="stToolbar"] { display: none !important; }
    .stMarkdown { font-size: 11pt; }
    h1, h2 { page-break-after: avoid; }
    table { page-break-inside: avoid; }
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="incorp-sticky">
    <h1>🏛️ Incorporation Agent</h1>
    <p>Entity type, state of formation, registered agent, filing checklist.
    All fields marked with <span style="color:#ef4444">*</span> are required.</p>
</div>
""",
    unsafe_allow_html=True,
)


# ── Print button helper (uses an iframe component to call window.parent.print) ──
def render_print_button(key: str) -> None:
    """Render a print/save-as-PDF button. Triggers the browser's print
    dialog on the parent Streamlit page (Save as PDF works the same way).
    """
    components.html(
        """
<div class="print-row" style="margin: 0.5rem 0;">
  <button
    onclick="window.parent.print()"
    style="
        background: #ef4444;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        cursor: pointer;
        font-size: 0.95rem;
        font-weight: 500;
    "
    onmouseover="this.style.background='#dc2626'"
    onmouseout="this.style.background='#ef4444'"
  >🖨️ Print / Save as PDF / Email</button>
  <span style="margin-left: 0.5rem; color: #888; font-size: 0.85rem;">
    Use your browser's print dialog to save as PDF or send to email.
  </span>
</div>
""",
        height=60,
    )


# ── Form ───────────────────────────────────────────────────────────────
with st.form("incorporation_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(
            "Business name" + _REQ,
            placeholder="Acme Bookkeeping",
        )
        state = st.text_input(
            "Founder's home state" + _REQ,
            placeholder="Texas",
        )
        cofounders = st.number_input(
            "Number of cofounders (including you)" + _REQ,
            min_value=1,
            max_value=20,
            value=1,
        )
    with col2:
        funding = st.selectbox(
            "Funding plans" + _REQ,
            [
                _UNSET,
                "Bootstrap (no outside funding)",
                "SAFE / friends & family",
                "Priced seed round (9–18 months)",
                "Priced Series A+ (12–36 months)",
            ],
        )
        employees = st.selectbox(
            "Hiring plans (12 months)" + _REQ,
            [
                _UNSET,
                "Just founders",
                "1–5 employees",
                "6+ employees",
            ],
        )

    description = st.text_area(
        "What does the business do? Any liability concerns?" + _REQ,
        placeholder="e.g. SaaS for auto-body shops; we store customer financial records.",
        height=120,
    )

    submitted = st.form_submit_button(
        "Create incorporation plan",
        type="primary",
    )


# ── Validation + run + render ──────────────────────────────────────────
if submitted:
    missing: list[str] = []
    if not name.strip():
        missing.append("Business name")
    if not state.strip():
        missing.append("Founder's home state")
    if funding == _UNSET:
        missing.append("Funding plans")
    if employees == _UNSET:
        missing.append("Hiring plans (12 months)")
    if not description.strip():
        missing.append("What does the business do?")

    if missing:
        st.error(
            "Please fill in the following required field"
            + ("s" if len(missing) > 1 else "")
            + ": "
            + ", ".join(missing)
            + "."
        )
        st.stop()

    full_input = (
        f"Business: {name.strip()}\n"
        f"Founder home state: {state.strip()}\n"
        f"Cofounders: {cofounders}\n"
        f"Funding plans: {funding}\n"
        f"Hiring plans (12 mo): {employees}\n\n"
        f"Description: {description.strip()}"
    )
    with st.spinner("Creating your incorporation plan..."):
        result = asyncio.run(run(full_input))

    # Top action row: print + download, above the rendered plan.
    render_print_button(key="top")
    st.download_button(
        "📄 Download as markdown",
        result,
        file_name="incorporation_plan.md",
        key="dl_top",
    )

    st.markdown(result)

    # Bottom action row: same controls, so the user doesn't have to scroll
    # back up after reading the plan.
    st.divider()
    render_print_button(key="bottom")
    st.download_button(
        "📄 Download as markdown",
        result,
        file_name="incorporation_plan.md",
        key="dl_bottom",
    )
