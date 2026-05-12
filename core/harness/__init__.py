# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Reusable orchestration patterns ("harnesses") for multi-stage agents.

v1 ships SequentialHarness. ParallelHarness and LoopHarness are planned.
"""
from .sequential_harness import HarnessResult, SequentialHarness, Stage

__all__ = ["SequentialHarness", "Stage", "HarnessResult"]
