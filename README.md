# 🤖 AI-Native Business Apps

> **AI-native business apps you can actually run — clone, customize, incorporate.**

![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-green)
![Provider-agnostic](https://img.shields.io/badge/providers-claude%20%7C%20openai%20%7C%20gemini%20%7C%20xai%20%7C%20ollama-orange)
![Made for founders](https://img.shields.io/badge/made%20for-founders-purple)

**Incorporation · Business plan · Loans · Legal · Compliance · Marketing —
hand-built, provider-agnostic, Apache-2.0.**

[🚀 Quick Start](#-quick-start) · [📂 Browse Agents](#-starter-business-agents) · [📚 Walkthroughs](#-walkthroughs)

---

## 💡 Why this exists

Most founders' first 30 days are a slog of boring-but-unavoidable tasks:
incorporating, filing for an EIN, opening a bank account, drafting NDAs,
sourcing suppliers, applying for an SBA loan, getting a website live.
LLMs are perfect at most of this — but the existing agent repos either
need an API key for every run, or you're cobbling together half-working
LangChain snippets.

This repo is different:

- **Hand-built, not curated.** Every agent is original work, end-to-end
  tested, no scrapes from elsewhere.
- **3-command setup.** `git clone`, `pip install -e .`, `streamlit run …`.
  No accounts, no signups, no telemetry.
- **Provider-agnostic.** Edit one line in `config.yaml` to swap between
  Claude (subscription via Claude Max), OpenAI, Gemini, xAI, or local
  Ollama. Codex (ChatGPT subscription) is on the roadmap.
- **Apache-2.0.** Fork it. Sell it. No paywall.

The audience: solo founders and 2-person teams bootstrapping a business
who want AI baked in from day 0.

## 🚀 Quick Start

Two lines. One to install, one to run any agent:

```bash
pipx install git+https://github.com/RyanAlberts/ai-native-business-apps.git
agent incorporation
```

That's it. `agent` is an interactive launcher that auto-discovers every agent
in the repo and opens its Streamlit UI. Try:

```bash
agent                              # interactive picker
agent list                         # list all available agents
agent business-plan                # launch any agent by short name
agent inco --cli "Solo founder in Texas, SaaS for plumbers."  # one-shot CLI
```

### Prefer to develop locally?

```bash
git clone https://github.com/RyanAlberts/ai-native-business-apps.git
cd ai-native-business-apps && pip install -e .
agent
```

### Auth

If `claude` (the Claude Code CLI) is logged into your Claude Max / Pro
subscription, you're done — no API key needed for any Claude-based agent.
The subscription guard automatically recognizes Claude Code and Cursor's
OAuth env markers, so running from inside those IDEs Just Works.

For non-Claude providers, copy `.env.example` to `.env` and fill the
provider key you want (`OPENAI_API_KEY`, `GOOGLE_API_KEY`, etc.).

## 🖥️ Running from your IDE

The agents are vanilla Python — they run from any terminal. The table below
covers the four common dev environments and how subscription auth flows in each.

| Environment | Status | Notes |
|---|---|---|
| **Plain terminal + Claude Max** | ✅ verified | Run `claude login` once. Agents pick up subscription auth automatically. Nothing else to configure. |
| **[Claude Code app](https://claude.ai/code)** | ✅ verified | Open the repo in Claude Code. App injects an OAuth-refreshed `ANTHROPIC_API_KEY` that's tied to your subscription — our guard recognizes the `CLAUDECODE` / `CLAUDE_CODE_ENTRYPOINT` markers and lets it pass through. `CLAUDE.md` is auto-loaded as repo context. |
| **[Cursor](https://cursor.com)** | ✅ works | Open the repo. Cursor's terminal is unmodified — falls through to `claude` CLI auth. `.cursorrules` is auto-loaded as repo context for Cursor's chat. |
| **[Codex CLI](https://github.com/openai/codex)** | ✅ as a coding helper / ⏳ as a provider | Use Codex as an AI coding assistant in this repo — it'll execute Python commands in the terminal. *Using* Codex/ChatGPT subscription as the LLM provider for our agents (i.e. `provider: codex` in `config.yaml`) is a v1.1 stub — see `core/llm/codex.py` for the implementation roadmap. |

### Context files auto-loaded per IDE

- `CLAUDE.md` — Claude Code
- `AGENTS.md` — Codex CLI and the [`agents.md`](https://agents.md) standard
- `.cursorrules` — Cursor

All three point to each other and to the canonical repo context, so no matter
which tool a contributor is in, they get a consistent picture of the conventions.

## 🔥 Featured

| | Agent | What it does | Provider |
|---|---|---|---|
| 🏛️ | **[Incorporation Agent](starter_business_agents/incorporation_agent/)** | Pick entity type, state, registered agent; prepare EIN + filing docs. | claude ✅ |
| 📋 | **[Business Plan Implementation Manager](advanced_business_agents/multi_agent_apps/business_plan_implementation_manager/)** | Sequential 4-stage pipeline: market research → SWOT → strategy → 90-day roadmap. | claude ✅ |
| 💡 | **[Business Idea Validator (template)](_template/)** | Validate a startup idea in 60 seconds — problem, MVP, risks, first experiment. | claude ✅ |

## 📑 Table of Contents

- [📂 Starter Business Agents](#-starter-business-agents)
- [🚀 Advanced Business Agents](#-advanced-business-agents)
- [🛠️ Agent Harnesses](#%EF%B8%8F-agent-harnesses)
- [🧰 Skills](#-skills)
- [📱 LLM Apps](#-llm-apps)
- [📚 Walkthroughs](#-walkthroughs)
- [🔌 Providers](#-providers)
- [🤝 Contributing](#-contributing)

## 📂 Starter Business Agents

Single-agent apps that automate one founder task. Copy any folder to
extend — each is self-contained.

- 🏛️ **[Incorporation Agent](starter_business_agents/incorporation_agent/)** — entity-type + state selection, registered-agent recs, EIN prep. `claude ✅`
- *(Wave 3) Loan & Funding Application Agent — SBA readiness, grant matching, app packages.*
- *(Wave 3) Legal Doc Generator — operating agreement, NDA, IP assignment, ToS, privacy policy.*
- *(Wave 3) Bank & Insurance Setup Agent — business banking comparison, GL/E&O recs.*
- *(Wave 3) Compliance & Tax Setup Agent — sales-tax nexus, state filings, annual calendar.*

## 🚀 Advanced Business Agents

Multi-agent orchestration — pipelines, teams, sequential or parallel.

- 📋 **[Business Plan Implementation Manager](advanced_business_agents/multi_agent_apps/business_plan_implementation_manager/)** — sequential 4-stage: market research → SWOT → strategy → 90-day roadmap. `claude ✅`
- *(Wave 3) Website Launch Team — domain, brand, hosting, launch copy & checklist.*
- *(Wave 3) Supplier Sourcing Team — discovery, vetting, RFP, comparison matrix.*

## 🛠️ Agent Harnesses

Reusable orchestration patterns. Use them to compose your own multi-stage agents.

- **[SequentialHarness](core/harness/sequential_harness.py)** — strict-order pipeline; output of stage N feeds stage N+1. `verified ✅`
- *(Planned) ParallelHarness — fan out across independent agents, merge results.*
- *(Planned) LoopHarness — iterate until a condition is met.*

## 🧰 Skills

Small reusable tools any agent can compose. *(Coming in v1.1 — contribute yours!)*

## 📱 LLM Apps

Broader apps that use LLMs but aren't strictly "agents" (one-shot generators,
chat interfaces, etc.). *(Coming in v1.1.)*

## 📚 Walkthroughs

Narrative tutorials that explain how each agent works and how to customize it.
For v1 they live in-repo as `WALKTHROUGH.md` files; a hosted tutorial site
arrives in v1.1.

- [Building Your First AI-Native Business Agent](_template/WALKTHROUGH.md)
- [Incorporation Agent walkthrough](starter_business_agents/incorporation_agent/WALKTHROUGH.md)
- [Business Plan Implementation Manager walkthrough](advanced_business_agents/multi_agent_apps/business_plan_implementation_manager/WALKTHROUGH.md)

## 🔌 Providers

Every agent honors `config.yaml::provider`. v1 verification matrix:

| Provider | Default model | Auth | Status |
|---|---|---|---|
| **claude** | claude-sonnet-4-6 | Claude Max subscription (preferred) or API key | **verified ✅** |
| **openai** | gpt-4o | API key | working |
| **gemini** | gemini-2.0-flash | API key | working |
| **xai** | grok-2-latest | API key | community-supported |
| **ollama** | llama3.2 | local daemon | community-supported |
| **codex** | — | ChatGPT subscription via Codex CLI | stub (help wanted) |

## 🤝 Contributing

We accept new agents, harnesses, skills, walkthroughs, and provider-adapter
fixes. Every contribution must be hand-built original work, end-to-end tested,
and Apache-2.0. See [CONTRIBUTING.md](CONTRIBUTING.md).

## 🙏 Built by

[Ryan Alberts](https://github.com/RyanAlberts), with structural inspiration
from [`awesome-llm-apps`](https://github.com/Shubhamsaboo/awesome-llm-apps)
(see [NOTICE](NOTICE)). No code or prompts are copied from upstream — every
agent here is original work.

## ⭐ Star History

If this helped your business, a star helps me build more.
