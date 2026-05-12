# Repo Context — for AI coding agents (Codex, Cursor, Claude Code)

This file follows the [`agents.md`](https://agents.md) convention — a
standard way to give context to AI coding agents about a repo. Codex, Cursor,
Claude Code, and others read this file (or its companion `CLAUDE.md`,
`.cursorrules`).

## What this repo is

`ai-native-business-apps` — a public, Apache-2.0 collection of hand-built,
provider-agnostic AI agents for startup founders. Each agent automates a
single "boring but necessary" task in the founder's first 30 days
(incorporation, business plan, loan applications, legal docs, etc.).

## Provider abstraction

`core/llm/` has an LLMClient ABC and one adapter per provider:

| Provider | Auth mode | Verification | Adapter file |
|---|---|---|---|
| claude | subscription (default) or API key | **verified** | `core/llm/claude.py` |
| openai | API key | working | `core/llm/openai.py` |
| gemini | API key | working | `core/llm/gemini.py` |
| xai | API key (OpenAI-compatible) | community-supported | `core/llm/xai.py` |
| ollama | local daemon | community-supported | `core/llm/ollama.py` |
| codex | ChatGPT subscription via Codex CLI | **stub** | `core/llm/codex.py` |

Pick the provider for an agent in `<agent>/config.yaml::provider`. Default
model in `<agent>/config.yaml::model`. All other knobs (temperature,
max_tokens, MCP servers, allowed_tools) live there too.

## File layout (Codex / Cursor: this is your map)

```
ai-native-business-apps/
├── README.md                  # public-facing repo description
├── CLAUDE.md                  # Claude Code auto-context (richer detail)
├── AGENTS.md                  # this file
├── CONTRIBUTING.md
├── pyproject.toml             # one workspace
├── _template/                 # copy-paste scaffold for new agents
├── core/
│   ├── llm/                   # provider abstraction
│   ├── harness/               # reusable patterns (SequentialHarness)
│   └── config.py              # YAML loader
├── starter_business_agents/   # single-agent apps
│   └── incorporation_agent/
├── advanced_business_agents/  # multi-agent / sequential
│   └── multi_agent_apps/
│       └── business_plan_implementation_manager/
└── scripts/parity_run.py      # capture golden outputs across providers
```

Each agent folder follows the pattern:
`agent.py` + `app.py` + `prompts.py` + `tools.py` + `config.yaml` +
`README.md` + `WALKTHROUGH.md` + `PARITY.md` + `tests/golden.jsonl`.

## Conventions

- **Python 3.11+**, async-first (`agent.py::run` is always `async def`).
- **Apache-2.0 header** at the top of every Python file we author.
- **Provider-agnostic agents**: never `import openai` directly from agent code
  — go through `core.get_llm()`.
- **Tools as `core.Tool` dataclasses**, never as framework-specific calls.
- **Prompts as named constants** in `prompts.py`, never inline in agent code.
- **No LangChain / LangGraph / CrewAI / Agno dependencies.** Our provider
  abstraction is hand-rolled and stays ~200 lines. Don't add a fat
  framework dep.

## Running agents

From a terminal (Cursor / Claude Code / Codex / iTerm — all the same):

```bash
# CLI
python -m starter_business_agents.incorporation_agent.agent "your input"

# Streamlit
streamlit run starter_business_agents/incorporation_agent/app.py
```

The first time, run `pip install -e .` from the repo root.

## Auth notes per environment

| Environment | What works without setup | Notes |
|---|---|---|
| Plain terminal + Claude Max | ✅ Just works | Run `claude login` once; agents pick up auth. |
| Claude Code app | ✅ Just works | App injects OAuth-refreshed subscription token; guard recognizes it. |
| Cursor terminal | ✅ Just works | Cursor doesn't inject keys; falls through to `claude` CLI auth. |
| Cursor agent mode | ⚠️ Limited | Cursor's chat AI can read this repo but doesn't run our agents inline. Open a terminal to run. |
| Codex CLI | ⚠️ Stub | `core/llm/codex.py` is not implemented in v1. Codex CLI itself works as a coding aid in this repo; running our agents *with* Codex as the provider is roadmap. |

## When asked to add a new agent

Always copy `_template/` as the starting point. Do not write an agent from
scratch — it'll drift from conventions and miss something (golden tests,
PARITY.md, the subscription guard inheritance, etc.).

## When asked to add a new provider

Subclass `core.LLMClient` in `core/llm/<provider>.py`. Implement
`complete(system_prompt, user_message, tools)`. Wire it into
`core/llm/factory.py::get_llm`. Add to the README provider matrix and to
this file's table.

## Don't

- Don't commit unless the user explicitly asks. The repo owner has standing
  rules about git autonomy.
- Don't refactor `core/` to use LiteLLM or LangChain.
- Don't add a `requirements.txt` if the agent uses only root deps.
- Don't paste `ANTHROPIC_API_KEY` into `.env.example` or anywhere else.
  Subscription is default.
