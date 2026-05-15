# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Shared Streamlit UI helpers used across every agent app.

The agents in this repo share the same UX contract:
  - All fields required, with red `*` markers + a sentinel option in
    selectboxes so the user must explicitly choose.
  - A sticky page header that scrolls with the user, theme-aware
    (light + dark + Streamlit theme-attribute + OS prefers-color-scheme).
  - Print buttons at the top and bottom of the rendered result so users
    can save as PDF, email, or print.
  - Print-only CSS that hides forms / buttons / Streamlit chrome so the
    print output is just the agent's plan content.

This module is the single source of truth for those patterns. Each
agent's `app.py` is a thin wrapper that calls into here:

    from core.ui import (
        REQ, UNSET, inject_styles, sticky_header,
        print_button, download_button, validate_required,
    )

    inject_styles()
    sticky_header(
        emoji="🏛️",
        title="Incorporation Agent",
        caption="Entity type, state, registered agent, filing checklist.",
    )
    with st.form("incorp"):
        name = st.text_input("Business name" + REQ)
        ...
        submitted = st.form_submit_button("Create plan", type="primary")
    if submitted:
        validate_required({"Business name": name, ...})  # stops on missing
        ...
"""
from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components


# ── Public constants ──────────────────────────────────────────────────

# Required-field marker. Concatenate onto every input label, e.g.
# `st.text_input("Business name" + REQ)`.
REQ = " :red[*]"

# Sentinel option to prepend to every required selectbox. Forces an
# explicit choice — if the value still equals UNSET at submit time,
# the field is "missing".
UNSET = "— select one —"


# ── inject_styles ─────────────────────────────────────────────────────

_STYLES = """
<style>
/* Sticky header — theme-aware. Translucent backdrop so content scrolling
   under it is hinted but text stays readable. */
.ai-sticky {
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
.ai-sticky h1 {
    margin: 0 0 0.25rem 0;
    font-size: 1.6rem;
    color: inherit;
}
.ai-sticky p {
    margin: 0;
    font-size: 0.9rem;
    opacity: 0.85;
    color: inherit;
}

/* Dark mode — Streamlit's default dark background is rgb(14, 17, 23). */
@media (prefers-color-scheme: dark) {
    .ai-sticky {
        background: rgba(14, 17, 23, 0.92);
        color: rgb(250, 250, 250);
        border-bottom-color: rgba(255, 255, 255, 0.12);
    }
}

/* Belt-and-suspenders: explicit Streamlit theme-attribute selector
   wins over the OS-level @media when the user toggled theme manually. */
[data-theme="dark"] .ai-sticky,
.stApp[data-theme="dark"] .ai-sticky {
    background: rgba(14, 17, 23, 0.92);
    color: rgb(250, 250, 250);
    border-bottom-color: rgba(255, 255, 255, 0.12);
}

@media print {
    .ai-sticky {
        position: static !important;
        border: none !important;
        margin: 0 0 1rem 0 !important;
        padding: 0 !important;
        background: transparent !important;
        color: black !important;
        backdrop-filter: none !important;
    }
    .stForm,
    [data-testid="stFormSubmitButton"],
    .ai-print-row,
    .stDownloadButton { display: none !important; }
    header[data-testid="stHeader"],
    footer,
    [data-testid="stToolbar"] { display: none !important; }
    .stMarkdown { font-size: 11pt; }
    h1, h2 { page-break-after: avoid; }
    table { page-break-inside: avoid; }
}
</style>
"""


def inject_styles() -> None:
    """Inject the global stylesheet. Call once near the top of each app."""
    st.markdown(_STYLES, unsafe_allow_html=True)


# ── sticky_header ─────────────────────────────────────────────────────


def sticky_header(*, emoji: str, title: str, caption: str) -> None:
    """Render a sticky page header that pins to the top on scroll.

    Args:
        emoji: Single emoji prefix for the title (e.g. "🏛️").
        title: Page title (rendered as <h1>).
        caption: One-sentence description shown below the title.
    """
    st.markdown(
        f"""
<div class="ai-sticky">
    <h1>{emoji} {title}</h1>
    <p>{caption} All fields marked with
       <span style="color:#ef4444">*</span> are required.</p>
</div>
""",
        unsafe_allow_html=True,
    )


# ── print_button ──────────────────────────────────────────────────────


def print_button(*, key: str) -> None:
    """Render a print / save-as-PDF / email button via the iframe components API.

    Calling `window.parent.print()` triggers the browser's native print
    dialog on the parent Streamlit page. From there the user can save as
    PDF, send to email, or print. No server-side PDF generation.

    Args:
        key: Unique key per call site (e.g. "top", "bottom"). Streamlit
            doesn't use this for components.html, but we accept it to
            match the rest of Streamlit's API for clarity at the call site.
    """
    _ = key  # accepted for clarity; components.html doesn't dedupe by key
    components.html(
        """
<div class="ai-print-row" style="margin: 0.5rem 0;">
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
    Opens your browser's print dialog — save as PDF or send to email.
  </span>
</div>
""",
        height=60,
    )


# ── validate_required ─────────────────────────────────────────────────


def validate_required(fields: dict[str, object]) -> None:
    """Validate that every required field has a non-empty value.

    If any field is empty (`""`, `None`, or equal to `UNSET`), render an
    error message listing every missing field and call `st.stop()` so
    the agent does NOT run.

    Args:
        fields: A dict mapping the user-facing field label to its current
            value. Strings get `.strip()` applied before the emptiness
            check; non-strings are checked against `None` and `UNSET`.

    Example:
        validate_required({
            "Business name": name,
            "Founder's home state": state,
            "Funding plans": funding,
            "What does the business do?": description,
        })
    """
    missing: list[str] = []
    for label, value in fields.items():
        if value is None:
            missing.append(label)
            continue
        if isinstance(value, str):
            if not value.strip() or value == UNSET:
                missing.append(label)
            continue
        # Non-string values (e.g. number_input) are considered set if
        # they're not None — Streamlit's number_input always has a value
        # within bounds, so it's effectively always "set."

    if missing:
        plural = "s" if len(missing) > 1 else ""
        st.error(
            f"Please fill in the following required field{plural}: "
            + ", ".join(missing)
            + "."
        )
        st.stop()


# ── result_actions ────────────────────────────────────────────────────


def result_actions(*, markdown: str, filename: str, position: str) -> None:
    """Render the standard action row that wraps a generated plan.

    Shows: print button + download-as-markdown button. Called twice per
    page — once before the rendered plan, once after — so the user
    doesn't have to scroll back up to print or download.

    Args:
        markdown: The plan content the download button will write.
        filename: Suggested filename for the download (e.g. "plan.md").
        position: "top" or "bottom". Used as the unique key for
            Streamlit's download button to avoid duplicate-key errors.
    """
    print_button(key=position)
    st.download_button(
        "📄 Download as markdown",
        markdown,
        file_name=filename,
        key=f"dl_{position}",
    )
