# Changelog

All notable changes to this project are documented here. The format is
loosely based on [Keep a Changelog](https://keepachangelog.com/), and the
project aims to follow semantic versioning once it hits 1.0.

## [Unreleased]

### Added
- **Agent-native Founding Journey** — clone the repo, open it with the AI
  agent you already have (Claude Code, Codex, Cursor), say "start my
  founding journey", and the agent runs the full journey with no Python, no
  pipx, no custom harness: a runner contract (`CLAUDE.md` / `AGENTS.md`),
  ordered playbooks (`playbooks/00`–`06`) over the shared `company.json`,
  deterministic phase gates (`verify/journey_gate.sh`), and a `PROGRESS.md`
  resume system. The playbooks reference the same single-source files the
  Python journey composes (`prompts.py` briefs, `core/state_portals.py`,
  the deterministic tool logic in `tools.py`), so the two paths can't drift
  apart — and they share one `company.json`, so a founder can switch paths
  mid-journey. The existing `keel` CLI is unchanged.
- **Keel brand layer** (`core/brand.py`) — single source of truth for the
  product name; the `keel` CLI alongside the legacy `agent` command.
- **Unified `Company` profile** (`core/company.py`) — one portable profile
  threaded across every agent, with JSON persistence and formation-readiness
  checks. Threaded into every starter agent's `run()` and Streamlit app.
- **Prepare-to-submit artifacts** (`core/artifacts.py`) — agents emit real
  files: Markdown, printable HTML (→ Save as PDF), and RFC-5545 `.ics`
  calendars. No new dependencies.
- **⭐ Founding Journey** (`advanced_business_agents/multi_agent_apps/founding_journey/`)
  — the flagship orchestrator: one intake runs incorporation → 83(b) → legal
  docs → banking → compliance in real-world order and synthesizes a Day-0
  Formation Packet plus downloadable artifacts.
- **Shared utilities** (`core/util.py`) — canonical `normalize_state` /
  `state_code` / `slugify`.
- **Consistent legal disclaimer** — `DISCLAIMER` / `with_disclaimer`
  exported from `core`, applied across pages and the README.
- **Launch kit** (`docs/launch/`) — 6-week plan, Show HN, Product Hunt,
  X/Twitter thread, and LinkedIn drafts.
- **Reproducible dev env** — `.claude/settings.json` SessionStart hook +
  `scripts/dev_setup.sh` provision a `.venv` with `claude-agent-sdk`.

### Fixed
- **Agents run out of the box under root** — the Claude adapter's default
  `bypassPermissions` made the CLI pass `--dangerously-skip-permissions`,
  which it refuses under root/sudo (exit 1). `_permission_mode()` now
  auto-downgrades to `default` when `euid == 0`, while honoring an explicit
  `extra.permission_mode` or the `KEEL_PERMISSION_MODE` env var. Verified
  with a live Claude round-trip.
- **Corrected stale federal legal guidance** across agents (BOI/CTA, DOL
  2024 worker-classification rule, 83(b)), with a regression guard.
- **Founding Journey degrades gracefully** instead of crashing when a step
  fails.

### Changed
- README rebuilt around the Keel positioning, the Founding Journey, and a
  competitor comparison table. Quick Start now leads with the agent-native
  path ("run with the AI you already have"); pipx is the alternative.
- `CLAUDE.md` / `AGENTS.md` are now the Founding Journey **runner
  contract**; the contributor/repo context they used to hold moved to
  `docs/REPO_GUIDE.md`.
- The SessionStart dev-env hook is contributor-opt-in (`KEEL_DEV=1` or an
  existing `.venv`), so a founder's fresh clone never pip-installs
  anything.

## [0.1.0]
- Initial collection: 9 starter agents + 4 advanced multi-agent pipelines,
  hand-rolled provider abstraction (Claude verified; OpenAI/Gemini/xAI/Ollama
  working), Sequential + Parallel harnesses, hand-curated 50-state portal
  data.
