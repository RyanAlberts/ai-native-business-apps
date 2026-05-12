# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tools for the Business Plan Implementation Manager.

For Claude, the WebSearch built-in is enabled via `config.yaml::allowed_tools`
— no custom tool needed. For other providers (no built-in search), the agent
falls back to training-data reasoning and notes uncertainty in the output.

If you want web search across all providers, wire a Tavily / Firecrawl /
SerpAPI tool here and add it to `all_tools()`.
"""
from __future__ import annotations

from core import Tool


def all_tools() -> list[Tool]:
    return []
