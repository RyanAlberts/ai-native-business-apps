# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tools for the Supplier Sourcing Team — none in v1.

If you enable `WebSearch` in config.yaml::allowed_tools, the sourcing stage
can sniff for actual named suppliers in the category. Recommended for
production use; Claude-only built-in.
"""
from __future__ import annotations

from core import Tool


def all_tools() -> list[Tool]:
    return []
