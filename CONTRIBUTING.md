# Contributing

Thanks for thinking about contributing. This repo is for founders — keep that audience in mind.

## What we accept

- **New agents** that automate a real "boring" startup task (incorporation, compliance, sourcing, etc.) Original work only — no ports, no scrapes, no LLM-slop READMEs.
- **New harnesses** that codify a reusable orchestration pattern (parallel, hierarchical, loop, etc.).
- **New skills** — small, single-purpose tools (e.g. a domain-lookup skill) that any agent can compose.
- **Provider adapters** — fill in or improve adapters in `core/llm/` (Codex, Ollama, etc.).
- **Walkthrough markdowns** for existing agents that don't have one.

## Standards

Every agent or app must:

1. **Be provider-agnostic.** Read its provider/model from `config.yaml`; no hard-coded SDK clients in `agent.py`.
2. **Be end-to-end tested.** Include at least 3 golden prompts in `tests/golden.jsonl` and a `PARITY.md` filled out for at least one provider (`verified`).
3. **Be forkable.** Prompts live in `prompts.py` as named constants. Tools live in `tools.py` as small `@tool` functions. No magic.
4. **Be self-contained.** `requirements.txt` lists any extras beyond root deps. README explains run + customize in <300 words.
5. **Be Apache-2.0.** Add the Apache header to every source file you create.

## Workflow

1. Open an issue describing the agent and which folder it belongs in (`starter_business_agents/` for single-agent, `advanced_business_agents/multi_agent_apps/` for multi-agent).
2. Copy `_template/` to your new agent folder. Number it with the next available prefix.
3. Implement, test, write `WALKTHROUGH.md` and `PARITY.md`.
4. Run `python scripts/parity_run.py <your_agent> --provider claude` and paste the run path into `PARITY.md`.
5. Open a PR. Title: `add <agent name>`.

## Code style

- Python 3.11+, type hints encouraged, `ruff check` clean.
- Async-first — `agent.py::run` is an `async` function.
- Streamlit UIs only — keep apps approachable.

## What we don't accept (yet)

- New top-level categories. Add to existing buckets in v0.x.
- LangChain / LangGraph dependencies. The repo deliberately avoids heavy frameworks.
- Voice / realtime agents. They don't fit subscription auth cleanly.
