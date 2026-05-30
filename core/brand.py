# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Single source of truth for the product's brand.

The repository slug (`ai-native-business-apps`) and the Python package
(`core`, `starter_business_agents`, …) stay stable so existing `pip` /
`pipx` installs and inbound links never break. The *product* name lives
here and is rendered in CLIs, app headers, and docs.

To rename the product, change `NAME` (and optionally `TAGLINE`) here —
nothing else needs to move.
"""
from __future__ import annotations

# The product name. Used in the CLI banner and Streamlit headers.
NAME = "Keel"

# One-liner shown under the name. A keel is the structural backbone laid
# down first when building a ship — everything else is built on it. The
# founder "lays the keel" of their company with this toolkit.
TAGLINE = "The open-source AI back-office for founders."

# Longer positioning line for READMEs / landing copy.
PITCH = (
    "Incorporate, bank, and stay compliant from Day 0 — a fleet of "
    "hand-built AI agents that run on the Claude subscription you already "
    "pay for. The open-source alternative to Stripe Atlas."
)

# The console-script entry point users type. Kept in sync with
# pyproject.toml [project.scripts].
CLI = "keel"


# ── Legal disclaimer ──────────────────────────────────────────────────
#
# Keel produces drafts and educational guidance — not legal, tax, or
# financial advice. This one liner is the single source of truth for that
# message. It's shown once (subtly) on every page via ``ui.sticky_header``
# and appended once to every downloadable / printed / CLI deliverable via
# ``with_disclaimer`` so an exported packet still carries it out of band.
# Keep it short so it informs without nagging.
DISCLAIMER = (
    f"{NAME} generates drafts and general guidance, not legal, tax, or "
    "financial advice. Verify against official sources and consult a "
    "licensed professional before filing or acting on anything here."
)

# Hidden marker so ``with_disclaimer`` is idempotent — threading an
# agent's output back through another step (or re-exporting) never stacks
# duplicate footers.
_DISCLAIMER_MARKER = "<!-- keel-disclaimer -->"


def disclaimer_md() -> str:
    """The disclaimer as a markdown footer block (carries the marker)."""
    return f"\n\n---\n{_DISCLAIMER_MARKER}\n*⚠️ {DISCLAIMER}*\n"


def with_disclaimer(markdown: str) -> str:
    """Append the disclaimer footer to ``markdown`` exactly once.

    Idempotent (no-op if the marker is already present) and a no-op on
    empty input, so it's safe to apply at every export boundary without
    worrying about double-stacking.
    """
    if not markdown or _DISCLAIMER_MARKER in markdown:
        return markdown
    return markdown.rstrip() + disclaimer_md()


def banner() -> str:
    """Return a one-line banner for CLI headers."""
    return f"{NAME} — {TAGLINE}"
