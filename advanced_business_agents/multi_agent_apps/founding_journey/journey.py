# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""The Founding Journey orchestrator — the unified back-office.

This is the flagship: instead of running twelve agents one at a time and
re-typing the same facts into each, the founder fills in a single
``Company`` profile and the journey runs the core formation agents in the
correct real-world order, threading the profile (and each step's output)
through the next, then synthesizes one **Day-0 Formation Packet** plus
prepare-to-submit artifacts.

Architecture note — why this composes prompts, not ``agent.run()``:
each starter agent's ``run()`` builds its own ``get_llm()`` internally,
which would mean five separate clients and no way to inject a fake LLM for
tests. Instead we import each agent's *real* ``SYSTEM_PROMPT`` + ``all_tools``
(the actual domain logic, one source of truth) and drive them with a
single shared ``LLMClient``. So the journey is DRY, uses the same prompts
the standalone agents do, and is fully unit-testable offline.
"""
from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Awaitable, Callable

from core import (
    DISCLAIMER,
    ArtifactSet,
    Company,
    LLMClient,
    Tool,
    get_llm,
    ics_artifact,
    letter_html,
    load_config,
    markdown_artifact,
    slugify,
    with_disclaimer,
)

# Import the REAL domain prompts + tools from the standalone starter agents.
from starter_business_agents.bank_insurance_agent import prompts as bank_p
from starter_business_agents.bank_insurance_agent import tools as bank_t
from starter_business_agents.compliance_tax_agent import prompts as comp_p
from starter_business_agents.compliance_tax_agent import tools as comp_t
from starter_business_agents.election_83b_agent import prompts as e83_p
from starter_business_agents.election_83b_agent import tools as e83_t
from starter_business_agents.incorporation_agent import prompts as inc_p
from starter_business_agents.incorporation_agent import tools as inc_t
from starter_business_agents.legal_doc_agent import prompts as legal_p
from starter_business_agents.legal_doc_agent import tools as legal_t

from .prompts import PACKET_SYNTHESIS_PROMPT, STEP_INSTRUCTIONS


@dataclass
class JourneyStep:
    """One specialist stop on the founding journey."""

    key: str
    title: str
    emoji: str
    system_prompt: str
    tools_factory: Callable[[], list[Tool]]

    @property
    def instruction(self) -> str:
        return STEP_INSTRUCTIONS.get(self.key, "")


@dataclass
class StepResult:
    key: str
    title: str
    emoji: str
    output: str
    ok: bool = True       # False if the specialist step raised
    error: str = ""       # short error summary when ok is False


@dataclass
class JourneyResult:
    """Everything produced by one journey run."""

    company: Company
    steps: list[StepResult] = field(default_factory=list)
    packet_markdown: str = ""

    @property
    def final(self) -> str:
        """Alias so the CLI launcher (which prints ``.final``) works."""
        return self.packet_markdown

    @property
    def failed_steps(self) -> list[StepResult]:
        """Steps that errored out — empty on a fully successful run."""
        return [s for s in self.steps if not s.ok]

    def artifacts(self) -> ArtifactSet:
        """Bundle the prepare-to-submit deliverables for download."""
        return build_artifacts(self)


def default_steps() -> list[JourneyStep]:
    """The core Day-0 formation sequence, in real-world order."""
    return [
        JourneyStep("incorporation", "Incorporation", "🏛️", inc_p.SYSTEM_PROMPT, inc_t.all_tools),
        JourneyStep("election_83b", "83(b) Election", "📬", e83_p.SYSTEM_PROMPT, e83_t.all_tools),
        JourneyStep("legal_doc", "Founding Legal Docs", "📜", legal_p.SYSTEM_PROMPT, legal_t.all_tools),
        JourneyStep("bank_insurance", "Banking & Insurance", "🏦", bank_p.SYSTEM_PROMPT, bank_t.all_tools),
        JourneyStep("compliance_tax", "Compliance & Tax", "📋", comp_p.SYSTEM_PROMPT, comp_t.all_tools),
    ]


StepCallback = Callable[[StepResult], None] | Callable[[StepResult], Awaitable[None]]


async def _maybe_await(value):
    if inspect.isawaitable(value):
        await value


async def run_journey(
    company: Company,
    *,
    llm: LLMClient | None = None,
    steps: list[JourneyStep] | None = None,
    on_step: StepCallback | None = None,
) -> JourneyResult:
    """Run the founding journey for ``company``.

    Args:
        company: the shared profile; rendered into each step's context.
        llm: an ``LLMClient`` to drive every step. If ``None``, one is
            built from this agent's ``config.yaml`` (the production path).
            Tests inject a fake client here.
        steps: override the default formation sequence.
        on_step: called after each step completes — stream progress to a UI.
    """
    if llm is None:
        llm = get_llm(load_config(__file__))
    steps = steps or default_steps()

    profile = company.to_context()
    results: list[StepResult] = []
    # Running transcript so each step sees the decisions made upstream.
    transcript = ""

    for step in steps:
        user_message = (
            f"{profile}\n"
            f"{transcript}\n"
            f"## Your task in the founding journey\n{step.instruction}"
        ).strip()
        # One specialist failing (a slow/erroring call, a flaky tool) must
        # not sink the whole journey — the founder should still get a packet
        # from the steps that did succeed. Capture the failure as a degraded
        # StepResult and keep going; the transcript notes the gap so later
        # steps and the synthesis know that section is missing.
        try:
            output = await llm.complete(
                system_prompt=step.system_prompt,
                user_message=user_message,
                tools=step.tools_factory() or None,
            )
            sr = StepResult(step.key, step.title, step.emoji, output)
            transcript += f"\n\n## Completed — {step.emoji} {step.title}\n{output}\n"
        except Exception as exc:  # noqa: BLE001 — degrade, don't crash the run
            err = f"{type(exc).__name__}: {exc}"
            note = (
                f"This step could not be completed automatically ({err}). "
                "Re-run the journey or run this specialist agent on its own."
            )
            sr = StepResult(step.key, step.title, step.emoji, note, ok=False, error=err)
            transcript += (
                f"\n\n## Skipped — {step.emoji} {step.title} (failed)\n{note}\n"
            )
        results.append(sr)
        if on_step is not None:
            await _maybe_await(on_step(sr))

    # Final synthesis: one coherent packet from the specialist outputs. If
    # synthesis itself fails, fall back to a concatenation of the steps so
    # the run still produces a usable packet instead of raising.
    synthesis_input = (
        f"{profile}\n\n# Specialist outputs to synthesize\n{transcript}"
    )
    try:
        packet = await llm.complete(
            system_prompt=PACKET_SYNTHESIS_PROMPT,
            user_message=synthesis_input,
            tools=None,
        )
    except Exception as exc:  # noqa: BLE001 — fall back to a raw concatenation
        packet = _fallback_packet(company, results, f"{type(exc).__name__}: {exc}")

    return JourneyResult(company=company, steps=results, packet_markdown=packet)


def _fallback_packet(
    company: Company, steps: list[StepResult], error: str
) -> str:
    """Assemble a usable packet from step outputs when synthesis fails."""
    name = company.legal_name or company.dba or "your company"
    parts = [
        f"# Day-0 Formation Packet — {name}",
        "",
        (
            "> ⚠️ Automatic synthesis could not complete "
            f"({error}). Below are the raw outputs from each specialist step "
            "that did run, in order. Re-run the journey to get the "
            "synthesized executive summary."
        ),
    ]
    for step in steps:
        status = "" if step.ok else " (failed)"
        parts.append(f"\n## {step.emoji} {step.title}{status}\n\n{step.output}")
    return "\n".join(parts)


# ── deterministic deadline calendar ───────────────────────────────────


def deadlines_for(company: Company) -> list[dict]:
    """Compute the deadlines we can derive deterministically from facts.

    LLM prose is great for explaining deadlines but unreliable to parse
    into calendar entries, so the ``.ics`` is built from hard facts only.
    Events without a computable date are simply omitted (the packet's
    "Key Deadlines" table still covers the narrative ones).
    """
    events: list[dict] = []
    code = company.formation_state_code

    # 83(b): 30 days from stock issuance (use formation_date as a proxy).
    if company.formation_date:
        try:
            issued = date.fromisoformat(company.formation_date)
            postmark = issued + timedelta(days=30)
            events.append(
                {
                    "date": postmark.isoformat(),
                    "summary": "83(b) election postmark deadline (HARD)",
                    "description": (
                        "Mail the signed 83(b) election to the IRS, postmarked on "
                        "or before this date. There is no extension. Use certified "
                        "mail with return receipt."
                    ),
                }
            )
        except ValueError:
            pass

    # Delaware C-Corp franchise tax + annual report: due March 1.
    if code == "DE" and "corp" in (company.entity_type or "").lower():
        # Use this year's March 1 if it hasn't passed yet, otherwise next
        # year's. The naive ``year + 1`` skipped an imminent deadline for
        # anyone viewing between Jan 1 and March 1.
        today = date.today()
        year = today.year if today <= date(today.year, 3, 1) else today.year + 1
        events.append(
            {
                "date": f"{year}-03-01",
                "summary": "Delaware franchise tax + annual report due",
                "description": (
                    "File the annual report and pay franchise tax. Use the "
                    "Assumed Par Value Capital method to avoid an inflated bill."
                ),
            }
        )

    return events


def build_artifacts(result: JourneyResult) -> ArtifactSet:
    """Turn a completed journey into downloadable, ready-to-file files."""
    company = result.company
    slug = slugify(company.legal_name or company.dba or "company")
    artifacts = ArtifactSet()

    # The portable profile — re-loadable into any standalone agent.
    artifacts.add(
        markdown_artifact(
            "company.json", company.to_json(), label="Company profile (company.json)"
        )
    )

    # The master packet, as markdown and as a printable HTML page. Both
    # carry the disclaimer so the exported/printed packet says "verify
    # this" out of band: the markdown via a footer, the HTML via its meta
    # line (which prints at the top of the Save-as-PDF page).
    artifacts.add(
        markdown_artifact(
            "00-formation-packet.md",
            with_disclaimer(result.packet_markdown),
            label="Day-0 Formation Packet (Markdown)",
        )
    )
    artifacts.add(
        letter_html(
            "00-formation-packet.html",
            title=f"Day-0 Formation Packet — {company.legal_name or company.dba or slug}",
            body_text=result.packet_markdown,
            meta=f"Generated by Keel. ⚠️ {DISCLAIMER}",
            label="Day-0 Formation Packet (printable / Save-as-PDF)",
        )
    )

    # Each specialist's full output, numbered in journey order.
    for i, step in enumerate(result.steps, start=1):
        artifacts.add(
            markdown_artifact(
                f"{i:02d}-{step.key}.md",
                with_disclaimer(f"# {step.emoji} {step.title}\n\n{step.output}"),
                label=f"{step.emoji} {step.title}",
            )
        )

    # Deterministic compliance calendar (only if we have dated obligations).
    events = deadlines_for(company)
    if events:
        artifacts.add(
            ics_artifact(
                "compliance-deadlines.ics",
                events,
                label="Compliance deadlines (.ics — import to your calendar)",
            )
        )

    return artifacts
