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


def banner() -> str:
    """Return a one-line banner for CLI headers."""
    return f"{NAME} — {TAGLINE}"
