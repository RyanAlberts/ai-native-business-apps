# Claude Code — Repo Context

This file is auto-loaded by Claude Code when this repo is the working directory.

## What this repo is

`ai-native-business-apps` — a public, Apache-2.0 collection of hand-built,
provider-agnostic AI agents for founders bootstrapping a startup. Theme:
agents that automate the boring stuff (incorporation, business plan, loans,
website setup, supplier sourcing, legal docs, etc.).

## What this repo is NOT

- Not a port of any other repo. Structural inspiration from
  [`awesome-llm-apps`](https://github.com/Shubhamsaboo/awesome-llm-apps),
  but no upstream code or prompts are used. Every agent is original work.
- Not framework-dependent. We deliberately avoid LangChain, LangGraph,
  CrewAI, Agno, etc. — see `CONTRIBUTING.md`.
- Not paid-API-first. Every agent should work on a Claude Max subscription
  by default; API keys are an opt-in.

## Architecture in 30 seconds

```
core/
├── company.py      # Shared Company profile — the spine threaded across agents
├── artifacts.py    # Prepare-to-submit deliverables (md / printable HTML / .ics)
├── util.py         # Canonical normalize_state / state_code / slugify (dedup)
├── brand.py        # Product name in ONE place (brand layer; slug unchanged)
├── llm/            # Provider abstraction (Claude verified, others working/stub)
├── harness/        # Reusable patterns (Sequential + Parallel shipped)
├── tools/          # Shared MCP-style Tools
├── state_portals.py# Hand-curated 50-state + federal portal links & fees
├── ui.py           # Shared Streamlit UX contract (+ artifact_downloads)
└── config.py       # YAML loader

agents/             # Two top-level buckets:
├── starter_business_agents/         # single-agent apps
└── advanced_business_agents/        # multi-agent / sequential
    └── multi_agent_apps/founding_journey/  # ⭐ flagship orchestrator
```

The **product name is "Keel"** (`core/brand.py`) — a brand layer only; the
GitHub slug (`ai-native-business-apps`) and Python package names are
unchanged so installs/links don't break. The CLI ships as both `keel` and
the legacy `agent`.

The **Founding Journey** threads a single `Company` through the core
formation agents in real-world order and synthesizes a Day-0 packet. It
composes each starter agent's real `SYSTEM_PROMPT` + `all_tools` under one
injectable `LLMClient` (DRY + offline-testable) — it does NOT call their
`run()`.

Each agent folder is self-contained:
```
agent.py        # importable async `run(input) -> result`
app.py          # Streamlit wrapper
prompts.py      # system + role prompts as constants
tools.py        # custom Tool definitions
config.yaml     # provider, model, MCP servers, allowed_tools
README.md       # how to run / customize
WALKTHROUGH.md  # narrative tutorial
PARITY.md       # provider-by-provider verification status
tests/golden.jsonl
```

## Claude-specific notes

- The subscription guard at `core/llm/claude.py::_enforce_subscription_guard`
  is whitelist-aware: if `CLAUDECODE`, `CLAUDE_CODE_ENTRYPOINT`, or
  `CLAUDE_CODE_SDK_HAS_OAUTH_REFRESH` is set in the env, an
  `ANTHROPIC_API_KEY` is assumed to be an OAuth-refreshed subscription
  token and passes through. So running agents from inside this app works
  without manual env tweaking.
- Default model is `claude-sonnet-4-6` (set in `pyproject.toml` env-var fallback).
  Override per-agent in `config.yaml::model` or globally via `CLAUDE_MODEL`.
- We use `claude-agent-sdk`'s built-in tool routing — MCP servers and
  `allowed_tools` are configured per-agent in `config.yaml`.

## Coding conventions

- Python 3.11+. Type hints encouraged but not enforced.
- All async — `agent.py::run` is always `async def`.
- One Apache-2.0 header at the top of every Python file we author.
- Streamlit for UIs; never anything heavier.
- No requirements.txt diff unless the agent genuinely needs an extra dep
  beyond what's in `pyproject.toml`.

## Common tasks

| Task | Command |
|---|---|
| Install in dev mode | `pip install -e .` |
| Run an agent (CLI) | `python -m starter_business_agents.incorporation_agent.agent "..."` |
| Run an agent (Streamlit) | `streamlit run starter_business_agents/incorporation_agent/app.py` |
| Capture parity baseline | `python scripts/parity_run.py <agent_module>` |
| Verify Claude auth works | `python -c "from core import get_llm, LLMConfig; get_llm(LLMConfig(provider='claude', model='claude-sonnet-4-6'))"` |

## When asked to add a new agent

1. Copy `_template/` to the right folder (`starter_business_agents/` for
   single-agent; `advanced_business_agents/multi_agent_apps/` for multi-stage).
2. Update `prompts.py`, `tools.py`, `config.yaml`, `agent.py::run()`'s
   signature and docstring.
3. Write 3–5 golden prompts in `tests/golden.jsonl`.
4. Fill out `README.md`, `WALKTHROUGH.md`, `PARITY.md` (mark Claude
   `verified` only after running it).
5. Add a row to the main `README.md`'s agent listing.

## Verification before declaring done

- Agent imports cleanly: `python -c "from <pkg> import run"`
- Agent runs end-to-end: `python -m <pkg>` produces output
- `PARITY.md` reflects what was actually run, not what we hoped would run

## What NOT to do

- Don't refactor `core/` to use LiteLLM or LangChain — provider abstraction
  is intentionally hand-rolled and lightweight.
- Don't add Docker / monorepo tooling in v1.
