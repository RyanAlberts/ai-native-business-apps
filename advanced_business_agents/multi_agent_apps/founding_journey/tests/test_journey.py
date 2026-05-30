# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Offline tests for the Founding Journey orchestrator.

These drive the journey with a fake LLMClient so the full pipeline —
step ordering, context threading, synthesis, and artifact generation —
is verified without any network or Claude auth.
"""
from __future__ import annotations

import asyncio
import json

from core import Company, LLMClient, LLMConfig

from advanced_business_agents.multi_agent_apps.founding_journey.journey import (
    deadlines_for,
    default_steps,
    run_journey,
)


class FakeLLM(LLMClient):
    """Records every call; echoes a tagged response per system prompt."""

    def __init__(self):
        super().__init__(LLMConfig(provider="fake", model="fake"))
        self.calls: list[dict] = []

    async def complete(self, system_prompt, user_message, tools=None):
        self.calls.append(
            {"system": system_prompt, "user": user_message, "tools": tools}
        )
        # Identify the synthesis step by its distinctive prompt header.
        if "Day-0 Formation Packet" in system_prompt:
            return "## 🎯 Executive Summary\nSynthesized packet."
        return f"OUTPUT[len={len(system_prompt)}]"


def _company():
    return Company(
        legal_name="Northwind Robotics, Inc.",
        one_liner="Warehouse robots",
        home_state="California",
        state_of_formation="Delaware",
        entity_type="C-Corp",
        formation_date="2026-06-01",
    )


def test_journey_runs_all_steps_plus_synthesis():
    llm = FakeLLM()
    result = asyncio.run(run_journey(_company(), llm=llm))
    # 5 specialist steps + 1 synthesis call.
    assert len(llm.calls) == 6
    assert len(result.steps) == 5
    assert [s.key for s in result.steps] == [
        "incorporation",
        "election_83b",
        "legal_doc",
        "bank_insurance",
        "compliance_tax",
    ]
    assert "Synthesized packet" in result.final


def test_company_profile_is_in_every_step_context():
    llm = FakeLLM()
    asyncio.run(run_journey(_company(), llm=llm))
    for call in llm.calls:
        assert "Northwind Robotics" in call["user"]


def test_context_threads_forward():
    """Step N should see the outputs of steps < N (decisions upstream)."""
    llm = FakeLLM()
    asyncio.run(run_journey(_company(), llm=llm))
    # The 2nd specialist call must contain the 1st step's completion header.
    second_step_user = llm.calls[1]["user"]
    assert "Completed — 🏛️ Incorporation" in second_step_user


def test_on_step_callback_fires_per_step():
    llm = FakeLLM()
    seen = []
    asyncio.run(run_journey(_company(), llm=llm, on_step=lambda sr: seen.append(sr.key)))
    assert seen == ["incorporation", "election_83b", "legal_doc", "bank_insurance", "compliance_tax"]


def test_artifacts_are_generated():
    llm = FakeLLM()
    result = asyncio.run(run_journey(_company(), llm=llm))
    arts = result.artifacts()
    names = {a.filename for a in arts}
    assert "company.json" in names
    assert "00-formation-packet.md" in names
    assert "00-formation-packet.html" in names
    assert "01-incorporation.md" in names
    assert "compliance-deadlines.ics" in names  # DE C-Corp + formation_date
    # company.json artifact round-trips back into a Company.
    profile = next(a for a in arts if a.filename == "company.json")
    assert json.loads(profile.content)["legal_name"] == "Northwind Robotics, Inc."


def test_deadlines_83b_and_de_franchise():
    events = deadlines_for(_company())
    summaries = " ".join(e["summary"] for e in events)
    assert "83(b)" in summaries
    assert "Delaware franchise tax" in summaries
    # 83(b) postmark = formation_date + 30 days.
    postmark = next(e for e in events if "83(b)" in e["summary"])
    assert postmark["date"] == "2026-07-01"


def test_deadlines_empty_without_dates():
    assert deadlines_for(Company(legal_name="X")) == []


def test_default_steps_shape():
    steps = default_steps()
    assert len(steps) == 5
    assert all(s.system_prompt and s.instruction for s in steps)


# ── resilience ─────────────────────────────────────────────────────────


class FailingStepLLM(LLMClient):
    """Fails on the legal-docs step; succeeds (incl. synthesis) otherwise."""

    def __init__(self):
        super().__init__(LLMConfig(provider="fake", model="fake"))

    async def complete(self, system_prompt, user_message, tools=None):
        if "Day-0 Formation Packet" in system_prompt:
            return "## 🎯 Executive Summary\nSynthesized from what ran."
        # The legal-doc step's instruction mentions an operating agreement /
        # founding docs; key off the prompt to fail exactly one specialist.
        from starter_business_agents.legal_doc_agent import prompts as legal_p

        if system_prompt == legal_p.SYSTEM_PROMPT:
            raise RuntimeError("simulated specialist timeout")
        return "ok"


class FailingSynthesisLLM(LLMClient):
    """Every specialist succeeds; only the final synthesis call blows up."""

    def __init__(self):
        super().__init__(LLMConfig(provider="fake", model="fake"))

    async def complete(self, system_prompt, user_message, tools=None):
        if "Day-0 Formation Packet" in system_prompt:
            raise RuntimeError("simulated synthesis failure")
        return "specialist ok"


def test_one_failing_step_does_not_sink_the_run():
    result = asyncio.run(run_journey(_company(), llm=FailingStepLLM()))
    # All five steps are still represented; exactly one is flagged failed.
    assert len(result.steps) == 5
    failed = result.failed_steps
    assert [s.key for s in failed] == ["legal_doc"]
    assert not failed[0].ok
    assert "simulated specialist timeout" in failed[0].error
    # Synthesis still ran and produced a packet.
    assert "Synthesized from what ran" in result.final


def test_failed_step_is_still_in_artifacts():
    result = asyncio.run(run_journey(_company(), llm=FailingStepLLM()))
    names = {a.filename for a in result.artifacts()}
    # The failed step still gets a numbered markdown file (with its note).
    assert "03-legal_doc.md" in names


def test_synthesis_failure_falls_back_to_concatenation():
    result = asyncio.run(run_journey(_company(), llm=FailingSynthesisLLM()))
    # No exception; the packet is the fallback concatenation of step outputs.
    assert "Automatic synthesis could not complete" in result.final
    assert "simulated synthesis failure" in result.final
    assert "🏛️ Incorporation" in result.final
    # And all five steps are recorded as successful.
    assert result.failed_steps == []
