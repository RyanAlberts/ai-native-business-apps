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
]
