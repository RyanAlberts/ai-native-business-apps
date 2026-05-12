# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""SequentialHarness — run a list of Stages in strict order, piping output forward.

Use for multi-step LLM workflows where each step depends on the previous step's
result. Example: Market Research -> SWOT -> Strategy -> Implementation Plan.

This is provider-agnostic: it takes any LLMClient and orchestrates `complete()`
calls. Composable: build the same pipeline against Claude (Max subscription) or
OpenAI (API key) by swapping the LLMClient.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Awaitable, Callable

from ..llm import LLMClient, Tool


@dataclass
class Stage:
    """One step in a sequential pipeline.

    Args:
        name: Human label for the stage (shown in UIs and logs).
        system_prompt: The system prompt the LLM uses for this stage.
        tools: Tools available to the LLM during this stage.
        input_template: Optional template applied to the previous stage's output
            before passing it to this stage. Use `{input}` as the placeholder.
            If None, the previous output is passed through as-is.
    """

    name: str
    system_prompt: str
    tools: list[Tool] = field(default_factory=list)
    input_template: str | None = None


@dataclass
class HarnessResult:
    """Result of a sequential pipeline run."""

    final: str
    stages: list[tuple[str, str]]  # [(stage_name, output), ...]


StageCallback = Callable[[str, str], None] | Callable[[str, str], Awaitable[None]]


class SequentialHarness:
    def __init__(self, llm: LLMClient, stages: list[Stage]):
        if not stages:
            raise ValueError("SequentialHarness needs at least one stage.")
        self.llm = llm
        self.stages = stages

    async def run(
        self,
        initial_input: str,
        on_stage_complete: StageCallback | None = None,
    ) -> HarnessResult:
        """Run all stages sequentially. `on_stage_complete(name, output)`
        is invoked after each stage — useful for streaming progress to a UI.
        """
        import inspect

        current = initial_input
        history: list[tuple[str, str]] = []
        for stage in self.stages:
            user_msg = (
                stage.input_template.format(input=current)
                if stage.input_template
                else current
            )
            output = await self.llm.complete(
                system_prompt=stage.system_prompt,
                user_message=user_msg,
                tools=stage.tools or None,
            )
            history.append((stage.name, output))
            if on_stage_complete is not None:
                ret = on_stage_complete(stage.name, output)
                if inspect.isawaitable(ret):
                    await ret
            current = output
        return HarnessResult(final=current, stages=history)
