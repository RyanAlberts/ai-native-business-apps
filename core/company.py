# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""The shared company profile — the spine of the unified product.

Every agent in this repo answers one slice of "what do I do on Day 0 of
my company?" In isolation each is useful; threaded together they become a
back-office. The thing that threads them is a single, portable
``Company`` profile: the founder fills it in once, and every agent reads
from it instead of re-asking for the same facts.

Design goals:
  * **Plain data, plain file.** A ``Company`` round-trips to a
    human-readable ``company.json`` you can commit, diff, and hand to the
    next agent. No database, no schema migration.
  * **Everything optional.** A founder on Day 0 knows their idea and home
    state but not their EIN yet. Agents fill fields in as they go
    (incorporation writes ``entity_type`` + ``state_of_formation``; the
    EIN step writes ``ein``; …).
  * **Two projections.** ``to_brief()`` renders the free-text description
    the single-agent ``run()`` functions already expect, so the profile
    drops into existing agents with zero changes to their signatures.
    ``to_context()`` renders a compact block to prepend to a system
    prompt.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, fields as dataclass_fields
from pathlib import Path

from .util import normalize_state

# Default on-disk location, overridable via the ``KEEL_COMPANY`` env var
# or an explicit path passed to ``load``/``save``.
DEFAULT_FILENAME = "company.json"


@dataclass
class Founder:
    """One founder / equity holder."""

    name: str = ""
    role: str = ""
    equity_pct: float | None = None
    email: str = ""


@dataclass
class Company:
    """A founder's company profile, shared across every agent.

    Fields map onto the questions the agents currently ask in their
    Streamlit forms — collected once, here, instead of per agent.
    """

    # Identity
    legal_name: str = ""
    dba: str = ""
    one_liner: str = ""           # what the business does, in a sentence
    industry: str = ""

    # Formation
    home_state: str = ""          # where the founders live / operate
    state_of_formation: str = ""  # where the entity is registered
    entity_type: str = ""         # "C-Corp", "LLC", "S-Corp", …
    formation_date: str = ""      # ISO date once filed
    ein: str = ""                 # once issued

    # People & money
    founders: list[Founder] = field(default_factory=list)
    funding_stage: str = ""       # "Bootstrap", "Priced seed", …
    employees_plan: str = ""      # "Just founders", "1–5", …

    # Free-form
    liability_notes: str = ""
    notes: str = ""

    # ── projections ───────────────────────────────────────────────────

    def to_brief(self) -> str:
        """Render the free-text founder description agents already expect.

        This is the bridge to the existing single-agent ``run()``
        functions: they take a free-text string, so we render one from
        structured state. Empty fields are omitted so the brief stays
        tight.
        """
        lines: list[str] = []
        name = self.legal_name or self.dba
        if name:
            lines.append(f"Business: {name}")
        if self.dba and self.dba != self.legal_name:
            lines.append(f"DBA / trade name: {self.dba}")
        if self.one_liner:
            lines.append(f"What it does: {self.one_liner}")
        if self.industry:
            lines.append(f"Industry: {self.industry}")
        if self.home_state:
            lines.append(f"Founder home state: {self.home_state}")
        if self.state_of_formation:
            lines.append(f"State of formation: {self.state_of_formation}")
        if self.entity_type:
            lines.append(f"Entity type: {self.entity_type}")
        if self.formation_date:
            lines.append(f"Formation date: {self.formation_date}")
        if self.ein:
            lines.append(f"EIN: {self.ein}")
        if self.founders:
            who = ", ".join(
                f"{f.name or 'Founder'}"
                + (f" ({f.role})" if f.role else "")
                + (f" — {f.equity_pct:g}%" if f.equity_pct is not None else "")
                for f in self.founders
            )
            lines.append(f"Founders ({len(self.founders)}): {who}")
        if self.funding_stage:
            lines.append(f"Funding plans: {self.funding_stage}")
        if self.employees_plan:
            lines.append(f"Hiring plans (12 mo): {self.employees_plan}")
        if self.liability_notes:
            lines.append(f"Liability concerns: {self.liability_notes}")
        if self.notes:
            lines.append(f"Notes: {self.notes}")
        return "\n".join(lines)

    def to_context(self) -> str:
        """Render a compact block to prepend to an agent's user message."""
        brief = self.to_brief()
        if not brief:
            return ""
        return (
            "## Known company profile\n"
            "Use these facts; do not re-ask for them. Treat blank fields as "
            "unknown and reason accordingly.\n\n"
            f"{brief}\n"
        )

    # ── validation / convenience ──────────────────────────────────────

    @property
    def formation_state_code(self) -> str | None:
        """Two-letter code for the state of formation (or home state)."""
        resolved = normalize_state(self.state_of_formation or self.home_state)
        return resolved[0] if resolved else None

    def missing_for_formation(self) -> list[str]:
        """Return the fields still needed before an entity can be filed."""
        needed = {
            "legal_name": self.legal_name,
            "home_state": self.home_state,
            "one_liner": self.one_liner,
        }
        return [k for k, v in needed.items() if not (v or "").strip()]

    # ── serialization ─────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Company":
        data = dict(data or {})
        founders = [
            f if isinstance(f, Founder) else Founder(**f)
            for f in data.pop("founders", []) or []
        ]
        known = {f.name for f in dataclass_fields(cls)}
        clean = {k: v for k, v in data.items() if k in known}
        return cls(founders=founders, **clean)

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_json(cls, text: str) -> "Company":
        return cls.from_dict(json.loads(text or "{}"))

    def save(self, path: str | Path | None = None) -> Path:
        target = Path(path) if path else _default_path()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.to_json() + "\n", encoding="utf-8")
        return target

    @classmethod
    def load(cls, path: str | Path | None = None) -> "Company":
        target = Path(path) if path else _default_path()
        if not target.exists():
            return cls()
        return cls.from_json(target.read_text(encoding="utf-8"))


def _default_path() -> Path:
    import os

    env = os.environ.get("KEEL_COMPANY")
    if env:
        return Path(env)
    return Path.cwd() / DEFAULT_FILENAME
