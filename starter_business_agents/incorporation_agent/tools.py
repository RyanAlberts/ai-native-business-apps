# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tools for the Incorporation Agent.

The agent reasons over the founder's input alone; no external tools are needed
for v1. If you want the agent to verify current state filing fees, add a
WebSearch entry to `config.yaml::allowed_tools` (Claude built-in) or wire a
custom `domain_lookup` / SoS scrape tool here.
"""
from __future__ import annotations

from core import Tool


def all_tools() -> list[Tool]:
    return []
