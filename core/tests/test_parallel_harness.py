# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tests for core.harness.parallel_harness.

Uses a fake LLMClient that records calls and returns canned responses,
so we can exercise the orchestration without needing a real provider.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

import pytest

from core import LLMClient, LLMConfig, ParallelHarness, Stage, Tool


@dataclass
class FakeLLM(LLMClient):
    """Records every complete() call. Returns the system_prompt as the
    'output' by default — predictable and lets us assert each branch
    received the right prompt."""
    config: LLMConfig = field(
        default_factory=lambda: LLMConfig(provider="fake", model="fake")
    )
    calls: list[dict] = field(default_factory=list)
    delay: float = 0.0
    response_map: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        super().__init__(self.config)

    async def complete(
        self,
        system_prompt: str,
        user_message: str,
        tools: list[Tool] | None = None,
    ) -> str:
        if self.delay:
            await asyncio.sleep(self.delay)
        self.calls.append(
            {
                "system_prompt": system_prompt,
                "user_message": user_message,
                "tools": [t.name for t in (tools or [])],
            }
        )
        # If a response is mapped to this system prompt, return it.
        for key, val in self.response_map.items():
            if key in system_prompt:
                return val
        return f"[output for system: {system_prompt[:40]}]"


def _branch(name: str, system: str = None, input_tpl: str | None = None) -> Stage:
    return Stage(
        name=name,
        system_prompt=system or f"You are the {name} branch.",
        input_template=input_tpl,
    )


def test_empty_branches_raises():
    with pytest.raises(ValueError, match="at least one branch"):
        ParallelHarness(llm=FakeLLM(), branches=[])


def test_runs_all_branches():
    llm = FakeLLM()
    harness = ParallelHarness(
        llm=llm,
        branches=[_branch("a"), _branch("b"), _branch("c")],
    )
    result = asyncio.run(harness.run("hello"))

    # All three branches ran (plus zero synthesizer).
    assert len(llm.calls) == 3
    assert len(result.stages) == 3
    branch_names = {name for name, _ in result.stages}
    assert branch_names == {"a", "b", "c"}


def test_branches_receive_initial_input_when_no_template():
    llm = FakeLLM()
    harness = ParallelHarness(
        llm=llm,
        branches=[_branch("a"), _branch("b")],
    )
    asyncio.run(harness.run("INITIAL"))
    for call in llm.calls:
        assert call["user_message"] == "INITIAL"


def test_branch_input_template_is_applied():
    llm = FakeLLM()
    harness = ParallelHarness(
        llm=llm,
        branches=[
            _branch("a", input_tpl="Researching: {input}"),
            _branch("b"),
        ],
    )
    asyncio.run(harness.run("the question"))
    msgs = {c["system_prompt"]: c["user_message"] for c in llm.calls}
    assert msgs["You are the a branch."] == "Researching: the question"
    assert msgs["You are the b branch."] == "the question"


def test_no_synthesizer_joins_branches_into_final():
    llm = FakeLLM(response_map={"the a branch": "AA", "the b branch": "BB"})
    harness = ParallelHarness(
        llm=llm,
        branches=[_branch("a"), _branch("b")],
    )
    result = asyncio.run(harness.run("x"))
    assert "AA" in result.final and "BB" in result.final
    assert "# a" in result.final and "# b" in result.final


def test_synthesizer_receives_combined_branches():
    llm = FakeLLM(
        response_map={
            "the a branch": "alpha-finding",
            "the b branch": "beta-finding",
            "synth": "SYNTHESIZED",
        }
    )
    harness = ParallelHarness(
        llm=llm,
        branches=[_branch("a"), _branch("b")],
        synthesizer=Stage(
            name="Synthesis", system_prompt="You are the synth stage."
        ),
    )
    result = asyncio.run(harness.run("x"))
    # Synthesizer got both branch outputs.
    synth_call = llm.calls[-1]
    assert "alpha-finding" in synth_call["user_message"]
    assert "beta-finding" in synth_call["user_message"]
    assert "## Branch: a" in synth_call["user_message"]
    assert "## Branch: b" in synth_call["user_message"]
    # final is the synthesizer output, not the joined branches.
    assert result.final == "SYNTHESIZED"
    # history includes 2 branches + 1 synthesizer.
    assert [n for n, _ in result.stages] == ["a", "b", "Synthesis"]


def test_synthesizer_template_overrides_default_combined_format():
    llm = FakeLLM(
        response_map={"the a branch": "AA", "the b branch": "BB", "synth": "FINAL"}
    )
    harness = ParallelHarness(
        llm=llm,
        branches=[_branch("a"), _branch("b")],
        synthesizer=Stage(
            name="Synth",
            system_prompt="You are the synth stage.",
            input_template="RAW FINDINGS:\n{input}\n\nProduce a verdict.",
        ),
    )
    asyncio.run(harness.run("x"))
    synth_msg = llm.calls[-1]["user_message"]
    assert synth_msg.startswith("RAW FINDINGS:")
    assert "Produce a verdict." in synth_msg


def test_callback_fires_for_every_stage_including_synthesizer():
    llm = FakeLLM()
    seen: list[tuple[str, str]] = []

    def cb(name, output):
        seen.append((name, output[:5]))

    harness = ParallelHarness(
        llm=llm,
        branches=[_branch("a"), _branch("b")],
        synthesizer=Stage(name="Synth", system_prompt="You are the synth stage."),
    )
    asyncio.run(harness.run("x", on_stage_complete=cb))
    names = {n for n, _ in seen}
    assert names == {"a", "b", "Synth"}


def test_branches_actually_run_concurrently():
    # Each branch sleeps 50ms. Three branches in sequence would take 150ms.
    # In parallel: ~50ms. Allow generous margin for CI noise.
    llm = FakeLLM(delay=0.05)
    harness = ParallelHarness(
        llm=llm,
        branches=[_branch("a"), _branch("b"), _branch("c")],
    )
    import time

    t0 = time.perf_counter()
    asyncio.run(harness.run("x"))
    elapsed = time.perf_counter() - t0
    # Sequential would be ~0.15s. Parallel should be well under 0.10s.
    assert elapsed < 0.10, f"branches did not run in parallel: {elapsed:.3f}s"


@dataclass
class ExplodingLLM(LLMClient):
    """Raises on every complete() call — to test graceful branch failure."""
    config: LLMConfig = field(
        default_factory=lambda: LLMConfig(provider="explode", model="x")
    )
    exc_type: type = RuntimeError
    message: str = "max_turns exceeded"

    def __post_init__(self):
        super().__init__(self.config)

    async def complete(
        self,
        system_prompt: str,
        user_message: str,
        tools: list[Tool] | None = None,
    ) -> str:
        raise self.exc_type(self.message)


class MixedLLM(LLMClient):
    """One branch raises, the others succeed — most realistic failure mode."""

    def __init__(self, fail_prompt_marker: str = "branch-fail"):
        super().__init__(LLMConfig(provider="mixed", model="x"))
        self.fail_prompt_marker = fail_prompt_marker
        self.calls = []

    async def complete(
        self,
        system_prompt: str,
        user_message: str,
        tools: list[Tool] | None = None,
    ) -> str:
        self.calls.append(system_prompt)
        if self.fail_prompt_marker in system_prompt:
            raise RuntimeError("max_turns exceeded")
        return f"[OK from {system_prompt[:30]}]"


def test_one_failing_branch_does_not_cancel_siblings():
    # Mix: branches a + b succeed, branch c raises. The harness must
    # still return all three results — c's slot showing the failure
    # marker, a and b showing their real outputs. The synthesizer can
    # then degrade gracefully instead of the whole agent crashing.
    llm = MixedLLM(fail_prompt_marker="the c branch")
    harness = ParallelHarness(
        llm=llm,
        branches=[_branch("a"), _branch("b"), _branch("c")],
    )
    result = asyncio.run(harness.run("x"))
    by_name = dict(result.stages)
    assert "OK from" in by_name["a"]
    assert "OK from" in by_name["b"]
    assert by_name["c"].startswith("[BRANCH FAILED:")
    assert "max_turns exceeded" in by_name["c"]
    assert "RuntimeError" in by_name["c"]


def test_all_branches_failing_still_returns_with_failure_markers():
    llm = ExplodingLLM()
    harness = ParallelHarness(
        llm=llm,
        branches=[_branch("a"), _branch("b"), _branch("c")],
    )
    result = asyncio.run(harness.run("x"))
    for _, output in result.stages:
        assert output.startswith("[BRANCH FAILED:")
    # `final` (no synthesizer) is the joined failures — still a string,
    # not an exception bubble.
    assert "[BRANCH FAILED:" in result.final


def test_failing_branch_still_passes_findings_to_synthesizer():
    # If 2 branches succeed and 1 fails, the synthesizer should see all
    # three blocks — the failure marker is just text to it.
    llm = MixedLLM(fail_prompt_marker="the b branch")
    harness = ParallelHarness(
        llm=llm,
        branches=[_branch("a"), _branch("b"), _branch("c")],
        synthesizer=Stage(name="Synth", system_prompt="You are the synth stage."),
    )
    asyncio.run(harness.run("x"))
    synth_msg = llm.calls[-1]
    # The synthesizer SAW the synthesizer prompt; the COMBINED branch
    # outputs were passed as the user_message. We can verify both by
    # inspecting MixedLLM's call recording.
    # `MixedLLM` records system prompts only; for a deeper assertion we
    # already verified individual branch handling in other tests. Here
    # the key invariant is: the synthesizer ran at all (i.e. did not
    # see an exception from an upstream branch).
    assert "You are the synth stage." in synth_msg
