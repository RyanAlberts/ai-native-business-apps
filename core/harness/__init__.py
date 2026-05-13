# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Reusable orchestration patterns ("harnesses") for multi-stage agents.

Ships SequentialHarness (pipeline) and ParallelHarness (fan-out then
synthesize). LoopHarness still planned.
"""
from .parallel_harness import ParallelHarness
from .sequential_harness import HarnessResult, SequentialHarness, Stage

__all__ = ["SequentialHarness", "Stage", "HarnessResult", "ParallelHarness"]
