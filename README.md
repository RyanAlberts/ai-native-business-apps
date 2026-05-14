# 🥇 AI-Native Business Apps — Build an AI-native business from Day 0.

**Ready-to-Run AI Agents for entrepreneurs & founders. Replace dozens of SaaS products with your very own fleet of agents that use the subscription you already pay for (Claude/OpenAI/Gemini or open-source models). No API key required.**

![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-green)
![Provider-agnostic](https://img.shields.io/badge/providers-claude%20%7C%20openai%20%7C%20gemini%20%7C%20xai%20%7C%20ollama-orange)
![Made for founders](https://img.shields.io/badge/made%20for-founders-purple)

**Incorporation · Business plan · Loans · Legal · Compliance · Marketing —
hand-built, provider-agnostic, Apache-2.0.**

[🚀 Quick Start](#-quick-start) · [📂 Browse Agents](#-starter-business-agents) · [📚 Walkthroughs](#-walkthroughs)

---

> **💎 Built on the [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk).** Every agent
> in this repo is built on `claude-agent-sdk`. Starting **June 15, 2026**, Claude **Max 20x**
> subscribers get a **$200/month credit** for Claude Agent SDK usage — *including third-party
> apps built on the SDK*. Agent SDK calls draw from this separate budget; your interactive
> Claude Code / Cowork / chat limits stay untouched. Translation: every Max 20x user can run
> every agent in this repo for $0 marginal cost, up to $200/mo. ([details](https://www.claude.com/legal/commercial-terms))

## 💡 Why this exists

Most founders' first 30 days are a slog of boring-but-unavoidable tasks:
incorporating, filing for an EIN, opening a bank account, drafting NDAs,
sourcing suppliers, applying for an SBA loan, getting a website live.
LLMs are perfect at most of this — but the existing agent repos either
need an API key for every run, or you're cobbling together half-working
LangChain snippets.

This repo is different:

- **Built on Claude Agent SDK — runs on your existing subscription.**
  No extra API spend, no LangChain, no bespoke LLM wrapper. The SDK is
  the platform; we just curate the agents on top. From **June 15, 2026**,
  Max 20x SDK calls (including from third-party apps like this one) draw
  on a separate **$200/mo credit** — interactive Claude Code / Cowork /
  chat limits stay reserved.
- **Hand-built, not curated.** Every agent is original work, end-to-end
  tested, no scrapes from elsewhere.
- **3-command setup.** `git clone`, `pip install -e .`, `streamlit run …`.
  No accounts, no signups, no telemetry.
- **Provider-agnostic.** Edit one line in `config.yaml` to swap between
  Claude (default, via Agent SDK), OpenAI, Gemini, xAI, or local Ollama.
  Codex (ChatGPT subscription) is on the roadmap.
- **Apache-2.0.** Fork it. Sell it. No paywall.

The audience: solo founders and small teams bootstrapping a business
who want AI baked in from day 0.

## 🚀 Quick Start

One line to install, one to run any agent in a Streamlit app that opens in your browser. (See [prerequisites](#-prerequisites) first if you're starting from scratch.)

```bash
pipx install git+https://github.com/RyanAlberts/ai-native-business-apps.git
agent incorporation
```
---

![Quick start screenshot — `agent incorporation` running in Streamlit](docs/screenshots/quick-start.png)

--- 

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
| 💰 | **[Loan & Funding Application Agent](starter_business_agents/loan_application_agent/)** | Match SBA loans / grants / CDFIs to your business; get an application checklist. | claude ✅ |

## 📑 Table of Contents

- [📂 Starter Business Agents](#-starter-business-agents)
- [🚀 Advanced Business Agents](#-advanced-business-agents)
- [🛠️ Agent Harnesses](#%EF%B8%8F-agent-harnesses)
- [🧰 Skills](#-skills)
- [📱 LLM Apps](#-llm-apps)
- [📚 Walkthroughs](#-walkthroughs)
- [💎 Built on Claude Agent SDK](#-built-on-claude-agent-sdk)
- [✅ Prerequisites](#-prerequisites)
- [🔌 Providers](#-providers)
- [🤝 Contributing](#-contributing)

## 📂 Starter Business Agents

Single-agent apps that automate one founder task. Run with `agent <short-name>`
or copy the folder to extend — each is self-contained.

| | Agent | What it does | Short name |
|---|---|---|---|
| 🏛️ | [Incorporation Agent](starter_business_agents/incorporation_agent/) | Entity type + state + registered agent + filing checklist. | `incorporation` |
| 📬 | [83(b) Election Agent](starter_business_agents/election_83b_agent/) | 30-day IRS §83(b) election letter + postmark deadline + service-center routing + calendar reminder. | `election-83b` |
| 🏛️ | [Delaware Franchise Tax Calculator](starter_business_agents/delaware_franchise_tax_agent/) | Recompute that $85K DE C-Corp bill under both methods — APVC typically lands at $400. | `delaware-franchise-tax` |
| 👥 | [Worker Classification Agent](starter_business_agents/worker_classification_agent/) | 1099 contractor or W-2 employee? IRS + DOL 2024 + state ABC tests with risk score. | `worker-classification` |
| 📋 | [Business License + DBA Agent](starter_business_agents/business_license_agent/) | Every license/permit/DBA you need at federal/state/county/city for your industry + city + state. | `business-license` |
| 💰 | [Loan & Funding Application Agent](starter_business_agents/loan_application_agent/) | Match SBA / microloan / grant / CDFI programs, prep package. | `loan` |
| 📜 | [Legal Document Generator](starter_business_agents/legal_doc_agent/) | Operating agreement, NDA, IP assignment, ToS, contractor agreement. | `legal-doc` |
| 🏦 | [Bank & Insurance Setup Agent](starter_business_agents/bank_insurance_agent/) | Business banking comparison + insurance policies you actually need. | `bank-insurance` |
| 📋 | [Compliance & Tax Setup Agent](starter_business_agents/compliance_tax_agent/) | Sales-tax nexus, state registrations, annual calendar, bookkeeping. | `compliance-tax` |

## 🚀 Advanced Business Agents

Multi-agent orchestration — sequential pipelines built on `core.SequentialHarness`.

| | Agent | Pipeline | Short name |
|---|---|---|---|
| 📋 | [Business Plan Implementation Manager](advanced_business_agents/multi_agent_apps/business_plan_implementation_manager/) | Market Research → SWOT → Strategy → 90-day Roadmap | `business-plan` |
| 🌐 | [Website Launch Team](advanced_business_agents/multi_agent_apps/website_launch_team/) | Brand & Domain → Site Architecture → Copy & Design → Launch Checklist | `website-launch` |
| 🏭 | [Supplier Sourcing Team](advanced_business_agents/multi_agent_apps/supplier_sourcing_team/) | Sourcing → Vetting → RFP Draft → Comparison Matrix | `supplier-sourcing` |
| ™️ | [Trademark Search Team](advanced_business_agents/multi_agent_apps/trademark_search_team/) | Federal TESS ∥ State SoS ∥ Common-Law ∥ Class ID → Synthesis (verdict + TEAS pre-fill + fee estimate) | `trademark-search` |

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

- [Building Your First AI-Native Business Agent](_template/WALKTHROUGH.md) (template)
- [Incorporation Agent walkthrough](starter_business_agents/incorporation_agent/WALKTHROUGH.md)
- [83(b) Election walkthrough](starter_business_agents/election_83b_agent/WALKTHROUGH.md)
- [Delaware Franchise Tax walkthrough](starter_business_agents/delaware_franchise_tax_agent/WALKTHROUGH.md)
- [Worker Classification walkthrough](starter_business_agents/worker_classification_agent/WALKTHROUGH.md)
- [Trademark Search Team walkthrough](advanced_business_agents/multi_agent_apps/trademark_search_team/WALKTHROUGH.md)
- [Business License + DBA walkthrough](starter_business_agents/business_license_agent/WALKTHROUGH.md)
- [Loan & Funding walkthrough](starter_business_agents/loan_application_agent/WALKTHROUGH.md)
- [Legal Document Generator walkthrough](starter_business_agents/legal_doc_agent/WALKTHROUGH.md)
- [Bank & Insurance Setup walkthrough](starter_business_agents/bank_insurance_agent/WALKTHROUGH.md)
- [Compliance & Tax Setup walkthrough](starter_business_agents/compliance_tax_agent/WALKTHROUGH.md)
- [Business Plan Implementation Manager walkthrough](advanced_business_agents/multi_agent_apps/business_plan_implementation_manager/WALKTHROUGH.md)
- [Website Launch Team walkthrough](advanced_business_agents/multi_agent_apps/website_launch_team/WALKTHROUGH.md)
- [Supplier Sourcing Team walkthrough](advanced_business_agents/multi_agent_apps/supplier_sourcing_team/WALKTHROUGH.md)

## 💎 Built on Claude Agent SDK

Every agent in this repo is a thin domain layer on top of
[`claude-agent-sdk`](https://docs.claude.com/en/api/agent-sdk). That's a
deliberate architectural choice — not LangChain, not LangGraph, not a
bespoke `claude -p` subprocess wrapper. Three reasons:

1. **Predictable billing for Max 20x users.** From June 15, 2026, every
   Agent SDK call (including from third-party tools like this repo) draws
   on the user's separate **$200/mo SDK credit**, not their interactive
   subscription cap. That makes "fork this repo + ship to your own
   audience" a viable distribution model with predictable economics.
2. **First-class tool routing via MCP.** The SDK speaks MCP natively, so
   our `core.Tool` abstraction wraps tools as `create_sdk_mcp_server`
   instances and the model gets clean structured tool-use messages back.
   No JSON-parsing of CLI stdout, no fragile prompt-engineering to coax
   tool calls.
3. **Session isolation.** `ClaudeAgentOptions(setting_sources=[])` lets
   each agent run in a clean Claude session, even when invoked from
   inside Claude Code or Cursor where the host has user-installed
   skills/plugins/hooks. No leakage, reproducible output.

### The canonical agent pattern (12 lines)

Every agent in this repo follows the same shape. Here it is from
[`_template/agent.py`](_template/agent.py), stripped to essentials:

```python
from claude_agent_sdk import query, ClaudeAgentOptions
from core import get_llm, load_config        # our thin abstraction
from .prompts import SYSTEM_PROMPT
from .tools import all_tools                  # list[core.Tool]

async def run(user_input: str) -> str:
    config = load_config(__file__)            # reads config.yaml
    llm = get_llm(config)                     # ClaudeClient by default
    return await llm.complete(
        system_prompt=SYSTEM_PROMPT,
        user_message=user_input,
        tools=all_tools(),
    )
```

`get_llm(config)` returns a `ClaudeClient` that internally constructs
`ClaudeAgentOptions(model=..., system_prompt=..., mcp_servers=...,
allowed_tools=..., setting_sources=[])` and iterates `query(prompt=...,
options=...)`. The SDK handles the tool loop; we just consume the final
`ResultMessage.result`. Multi-stage agents (business plan, website
launch, supplier sourcing) compose this primitive via
`SequentialHarness`.

### Why not `claude -p`?

Subprocess + stdout parsing works, but you lose: structured message
types, MCP tool routing, OAuth env detection for Claude Code / Cursor
contexts, and `setting_sources=[]` isolation. The SDK gives all four for
free. We keep a stub `core/llm/codex.py` adapter as the model for what a
subprocess-based provider would look like.

→ Start a new agent: copy [`_template/`](_template/), edit `prompts.py`,
`tools.py`, `config.yaml`. The SDK call shape never changes.

## ✅ Prerequisites

The [Quick Start](#-quick-start) assumes three things are installed and ready.
Most developers already have them; founders new to a terminal will need to
spend ~10 minutes setting them up once.

### 1. Python 3.11+

| OS | Install |
|---|---|
| macOS | `brew install python@3.11` (install [Homebrew](https://brew.sh/) first if needed) |
| Linux (Ubuntu/Debian) | `sudo apt install python3.11 python3.11-venv` |
| Windows | Download from [python.org/downloads](https://www.python.org/downloads/) — check "Add Python to PATH" during install |

Verify: `python3 --version` → should print `Python 3.11.x` or higher.

### 2. pipx

`pipx` installs CLI Python apps into isolated venvs so they don't pollute
your system Python.

| OS | Install |
|---|---|
| macOS | `brew install pipx && pipx ensurepath` |
| Linux | `python3 -m pip install --user pipx && python3 -m pipx ensurepath` |
| Windows | `python -m pip install --user pipx && python -m pipx ensurepath` |

After `ensurepath`, restart your terminal. Verify: `pipx --version`.

### 3. Auth for your provider

**Option A — Claude Max subscription (preferred, free):** install the
Claude Code CLI and log in.

```bash
npm install -g @anthropic-ai/claude-code   # requires Node.js — install from nodejs.org if needed
claude                                     # walks you through OAuth login on first run
```

The agents in this repo automatically pick up your subscription auth from
`claude`. No API key needed.

**Option B — Bring your own API key:** copy `.env.example` to `.env` and
fill the key for the provider you want (OpenAI, Gemini, etc.):

```bash
cp .env.example .env
# then edit .env and uncomment OPENAI_API_KEY=sk-... (or GOOGLE_API_KEY, etc.)
```

For per-agent provider overrides, edit `<agent>/config.yaml::provider`.

---

Once those three are in place, the [Quick Start](#-quick-start) install
command works.

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
