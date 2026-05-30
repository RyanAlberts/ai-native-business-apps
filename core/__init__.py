# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Core building blocks for AI-Native Business Apps.

Exports:
    load_config: read an agent's config.yaml from a path next to it
    get_llm: factory returning an LLMClient for the configured provider
    LLMClient, LLMConfig, Tool: building blocks for agent code
    SequentialHarness, Stage: reusable multi-stage pipeline
    ParallelHarness: fan-out N branches concurrently then synthesize
"""
from .config import load_config
from .llm import LLMClient, LLMConfig, Tool, get_llm
from .harness import HarnessResult, ParallelHarness, SequentialHarness, Stage
from .company import Company, Founder
from .artifacts import (
    Artifact,
    ArtifactSet,
    html_artifact,
    ics_artifact,
    letter_html,
    markdown_artifact,
    text_artifact,
)
from .util import normalize_state, slugify, state_code
from .brand import DISCLAIMER, with_disclaimer

__all__ = [
    "load_config",
    "get_llm",
    "LLMClient",
    "LLMConfig",
    "Tool",
    "SequentialHarness",
    "ParallelHarness",
    "Stage",
    "HarnessResult",
    # unified company spine
    "Company",
    "Founder",
    # prepare-to-submit artifacts
    "Artifact",
    "ArtifactSet",
    "markdown_artifact",
    "text_artifact",
    "html_artifact",
    "letter_html",
    "ics_artifact",
    # shared helpers
    "normalize_state",
    "state_code",
    "slugify",
    # brand / legal disclaimer
    "DISCLAIMER",
    "with_disclaimer",
]
