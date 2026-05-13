# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""ParallelHarness — fan out N branches concurrently, then synthesize.

Use for research-heavy workflows where you want N specialists to
investigate different angles in parallel and then a synthesizer to
consolidate findings into a single output.

Example: a trademark search where federal TESS, state-level registries,
common-law conflict scanning, and USPTO class identification all run in
parallel against the same proposed mark, and a synthesizer agent then
produces the likelihood-of-confusion report + TEAS application pre-fill.

Provider-agnostic — works against any `LLMClient` exactly like
`SequentialHarness`.
"""
from __future__ import annotations

import asyncio
import inspect

from ..llm import LLMClient
from .sequential_harness import HarnessResult, Stage, StageCallback


class ParallelHarness:
    """Run a list of branch Stages concurrently against the same initial
    input, then optionally pass their combined outputs through a
    synthesizer Stage.

    Args:
        llm: An LLMClient (any provider).
        branches: Stages that run in parallel. Each receives `initial_input`
            (formatted through its `input_template` if set).
        synthesizer: Optional final Stage. Receives a markdown-formatted
            concatenation of all branch outputs (one `## Branch: <name>`
            section per branch). If None, `final` is the joined branches.
    """

    def __init__(
        self,
        llm: LLMClient,
        branches: list[Stage],
        synthesizer: Stage | None = None,
    ):
        if not branches:
            raise ValueError("ParallelHarness needs at least one branch.")
        self.llm = llm
        self.branches = branches
        self.synthesizer = synthesizer

    async def run(
        self,
        initial_input: str,
        on_stage_complete: StageCallback | None = None,
    ) -> HarnessResult:
        """Run all branches concurrently, then synthesize.

        `on_stage_complete(stage_name, output)` is invoked after every
        branch and after the synthesizer — useful for streaming progress
        to a UI. Branch callbacks may fire in any order since branches
        race.
        """

        async def _run_branch(stage: Stage) -> tuple[str, str]:
            user_msg = (
                stage.input_template.format(input=initial_input)
                if stage.input_template
                else initial_input
            )
            output = await self.llm.complete(
                system_prompt=stage.system_prompt,
                user_message=user_msg,
                tools=stage.tools or None,
            )
            if on_stage_complete is not None:
                ret = on_stage_complete(stage.name, output)
                if inspect.isawaitable(ret):
                    await ret
            return stage.name, output

        branch_results = await asyncio.gather(
            *[_run_branch(b) for b in self.branches]
        )
        history: list[tuple[str, str]] = list(branch_results)

        if self.synthesizer is None:
            final = "\n\n---\n\n".join(
                f"# {name}\n\n{out}" for name, out in history
            )
            return HarnessResult(final=final, stages=history)

        combined = "\n\n".join(
            f"## Branch: {name}\n\n{out}" for name, out in history
        )
        synth_user_msg = (
            self.synthesizer.input_template.format(input=combined)
            if self.synthesizer.input_template
            else combined
        )
        synth_output = await self.llm.complete(
            system_prompt=self.synthesizer.system_prompt,
            user_message=synth_user_msg,
            tools=self.synthesizer.tools or None,
        )
        history.append((self.synthesizer.name, synth_output))
        if on_stage_complete is not None:
            ret = on_stage_complete(self.synthesizer.name, synth_output)
            if inspect.isawaitable(ret):
                await ret
        return HarnessResult(final=synth_output, stages=history)
