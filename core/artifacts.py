# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Prepare-to-submit artifacts.

The difference between "an LLM told me what to do" and "I have the thing
in my hand, ready to file" is the whole product. This module is the thin,
dependency-free layer that turns an agent's reasoning into real files a
founder can download and submit:

  * ``markdown_artifact`` / ``text_artifact`` — plain deliverables.
  * ``html_artifact`` — a self-contained, printable HTML page (the
    browser's "Save as PDF" turns it into a filing-ready PDF — no
    headless-Chrome or reportlab dependency).
  * ``ics_artifact`` — a real RFC-5545 calendar file for compliance
    deadlines (franchise tax, annual report, 83(b) postmark, …) that
    imports into Google/Apple/Outlook.

``ArtifactSet`` collects them; ``write(dir)`` drops them on disk and
returns a manifest. The Streamlit layer offers each as a download button;
the CLI writes them to an output folder.

We deliberately avoid heavy PDF libraries: printable HTML keeps the
3-command-setup promise intact and renders identically everywhere.
"""
from __future__ import annotations

import html as _html
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class Artifact:
    """A single downloadable deliverable."""

    filename: str
    content: str
    mimetype: str = "text/plain"
    label: str = ""           # human label for a download button

    def write(self, directory: str | Path) -> Path:
        path = Path(directory) / self.filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.content, encoding="utf-8")
        return path


@dataclass
class ArtifactSet:
    """An ordered collection of artifacts produced by one agent run."""

    artifacts: list[Artifact] = field(default_factory=list)

    def add(self, artifact: Artifact) -> "ArtifactSet":
        self.artifacts.append(artifact)
        return self

    def extend(self, others: "ArtifactSet | list[Artifact]") -> "ArtifactSet":
        items = others.artifacts if isinstance(others, ArtifactSet) else others
        self.artifacts.extend(items)
        return self

    def __iter__(self):
        return iter(self.artifacts)

    def __len__(self) -> int:
        return len(self.artifacts)

    def write(self, directory: str | Path) -> list[Path]:
        """Write every artifact to ``directory``; return the paths."""
        return [a.write(directory) for a in self.artifacts]

    def manifest(self) -> list[dict]:
        return [
            {"filename": a.filename, "mimetype": a.mimetype, "label": a.label}
            for a in self.artifacts
        ]


# ── builders ──────────────────────────────────────────────────────────


def text_artifact(filename: str, content: str, *, label: str = "") -> Artifact:
    return Artifact(filename=filename, content=content, mimetype="text/plain", label=label)


def markdown_artifact(filename: str, content: str, *, label: str = "") -> Artifact:
    return Artifact(
        filename=filename, content=content, mimetype="text/markdown", label=label
    )


_HTML_SHELL = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{title}</title>
<style>
  @page {{ margin: 1in; }}
  body {{ font: 12pt/1.5 -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
          max-width: 7.5in; margin: 1in auto; color: #111; }}
  h1, h2, h3 {{ line-height: 1.25; }}
  h1 {{ font-size: 20pt; }} h2 {{ font-size: 15pt; margin-top: 1.4em; }}
  pre {{ white-space: pre-wrap; background: #f6f8fa; padding: 1em; border-radius: 6px; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #d0d7de; padding: 6px 10px; text-align: left; }}
  .meta {{ color: #57606a; font-size: 10pt; margin-bottom: 2em; }}
  @media print {{ body {{ margin: 0; }} }}
</style></head>
<body>
<div class="meta">{meta}</div>
{body}
</body></html>
"""


def html_artifact(
    filename: str,
    *,
    title: str,
    body_html: str,
    meta: str = "",
    label: str = "",
) -> Artifact:
    """Wrap pre-rendered HTML in a printable, self-contained page."""
    doc = _HTML_SHELL.format(
        title=_html.escape(title),
        meta=_html.escape(meta),
        body=body_html,
    )
    return Artifact(filename=filename, content=doc, mimetype="text/html", label=label)


def letter_html(
    filename: str, *, title: str, body_text: str, meta: str = "", label: str = ""
) -> Artifact:
    """Render a plain-text letter/body as a printable HTML artifact.

    Paragraphs (blank-line separated) become ``<p>``; everything is
    escaped, so this is safe for arbitrary agent output.
    """
    paras = [
        "<p>" + _html.escape(p.strip()).replace("\n", "<br>") + "</p>"
        for p in body_text.split("\n\n")
        if p.strip()
    ]
    return html_artifact(
        filename, title=title, body_html="\n".join(paras), meta=meta, label=label
    )


def _ics_escape(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def ics_artifact(
    filename: str,
    events: list[dict],
    *,
    calendar_name: str = "Keel — Compliance Deadlines",
    label: str = "",
) -> Artifact:
    """Build an RFC-5545 ``.ics`` file from all-day deadline events.

    Each event dict: ``{"date": "YYYY-MM-DD", "summary": str,
    "description": str (optional)}``. Produces all-day VEVENTs so they
    import cleanly into any calendar.
    """
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Keel//ai-native-business-apps//EN",
        "CALSCALE:GREGORIAN",
        f"X-WR-CALNAME:{_ics_escape(calendar_name)}",
    ]
    for i, ev in enumerate(events):
        date = (ev.get("date") or "").replace("-", "")
        if len(date) != 8:
            continue  # skip malformed dates rather than emit a broken VEVENT
        lines += [
            "BEGIN:VEVENT",
            f"UID:keel-{stamp}-{i}@ai-native-business-apps",
            f"DTSTAMP:{stamp}",
            f"DTSTART;VALUE=DATE:{date}",
            f"SUMMARY:{_ics_escape(ev.get('summary', 'Deadline'))}",
        ]
        if ev.get("description"):
            lines.append(f"DESCRIPTION:{_ics_escape(ev['description'])}")
        lines += ["END:VEVENT"]
    lines.append("END:VCALENDAR")
    return Artifact(
        filename=filename,
        content="\r\n".join(lines) + "\r\n",
        mimetype="text/calendar",
        label=label,
    )
