<div align="center">

# ⚓ Keel

### The open-source AI back-office for founders.

**Incorporate, bank, and stay compliant from Day 0 — a fleet of hand-built AI agents that run on the Claude subscription you already pay for.**
**The open-source alternative to Stripe Atlas.**

![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-green)
![Providers](https://img.shields.io/badge/providers-claude%20%7C%20openai%20%7C%20gemini%20%7C%20xai%20%7C%20ollama-orange)
![Built on](https://img.shields.io/badge/built%20on-Claude%20Agent%20SDK-8A2BE2)
![No API key required](https://img.shields.io/badge/API%20key-not%20required-brightgreen)

[🚀 Quick Start](#-quick-start) · [⚓ The Founding Journey](#-the-founding-journey) · [🆚 vs Stripe Atlas](#-vs-stripe-atlas) · [📂 Agents](#-the-agent-fleet) · [💎 Built on Claude Agent SDK](#-built-on-the-claude-agent-sdk)

</div>

---

> **A keel** is the structural backbone laid down first when building a ship — everything else is built on it. Keel is what you lay down first when building a company.

> ⚠️ **Not legal, tax, or financial advice.** Keel generates drafts and general guidance to get you most of the way there. Verify everything against official sources and have a licensed professional review it before you file or act. Laws change and the agents can be wrong.

## ⚡ TL;DR

```bash
pipx install git+https://github.com/RyanAlberts/ai-native-business-apps.git
keel founding-journey
```

Fill in your company **once**. Get back a complete **Day-0 Formation Packet** — entity choice, 83(b) election letter, founding legal docs, banking & insurance plan, and a compliance calendar — plus the real, ready-to-file documents. On the Claude subscription you already pay for. No API key. No SaaS bill. Apache-2.0.

## 💡 Why Keel exists

A founder's first 30 days are a slog of boring-but-unavoidable back-office work: incorporate, file for an EIN, make the 83(b) election (miss the 30-day window and it's gone forever), draft an operating agreement, open a bank account, figure out sales-tax nexus, set up a compliance calendar.

Stripe Atlas does a slice of this — for a fee, in their walled garden, US-Delaware-C-Corp-only, and you don't own any of it. The rest you cobble together from LegalZoom upsells, a lawyer's hourly rate, and half-working LangChain snippets that demand an API key per run.

**Keel is different:**

- **It's a back office, not a bag of demos.** The flagship [Founding Journey](#-the-founding-journey) runs the whole formation sequence in the right order over one shared company profile — not twelve disconnected chatbots you re-explain yourself to.
- **It hands you the actual files.** "Prepare-to-submit," not "here's some advice": filled letters, an operating agreement, a real `.ics` compliance calendar, pre-filled official portal links. You review and submit.
- **It runs on the subscription you already have.** Built on the [Claude Agent SDK](#-built-on-the-claude-agent-sdk) — no extra API spend, no LangChain, no telemetry.
- **You own all of it.** Apache-2.0. Fork it, extend it, run it for your accelerator's whole batch. No paywall, ever.

## ⚓ The Founding Journey

The flagship. One structured intake → five specialists, threaded in real-world order → one synthesized packet.

```
company.json  ──►  🏛️  Incorporation        ┐
                   📬  83(b) Election         │  each step sees your profile
                   📜  Founding Legal Docs    │  + every decision made upstream
                   🏦  Banking & Insurance    │  (the operating agreement matches
                   📋  Compliance & Tax       ┘   the entity step 1 chose, etc.)
                            │
                            ▼
                   📦  Day-0 Formation Packet
                       ├─ ✅ Master Day-0 checklist (correctly ordered:
                       │     no EIN before the entity, no bank before the EIN…)
                       ├─ 📅 Key-deadlines table
                       ├─ 🔗 Deduplicated official portal links
                       └─ 📎 Documents prepared (sign / mail / file / keep)
```

**You download real files**, not a transcript:

| File | What it is |
|---|---|
| `00-formation-packet.html` | The whole packet as a printable page → **Save as PDF**. |
| `company.json` | Your portable profile — drop it into any standalone agent. |
| `01…05-*.md` | Each specialist's full output. |
| `compliance-deadlines.ics` | A real calendar file (83(b) postmark, franchise tax) → import to Google/Apple/Outlook. |

> Deadlines in the `.ics` are computed **deterministically** from your facts (formation date, state, entity type) — never parsed out of LLM prose — so the dates are trustworthy.

```bash
keel founding-journey                       # structured Streamlit intake
keel founding-journey --cli ./company.json  # or start from a saved profile
```

## 🆚 vs Stripe Atlas

|  | **Keel** | **Stripe Atlas** |
|---|---|---|
| Price | **$0** (runs on your Claude sub) | $500 one-time |
| Entity types | LLC · C-Corp · S-Corp · sole prop, **any state** | DE C-Corp / LLC only |
| 83(b) election | ✅ generates the letter + 30-day deadline calendar | ⚠️ filing assistance, C-Corp only |
| Founding legal docs | ✅ operating agreement / bylaws, IP assignment, NDA | partial (templates) |
| Banking & insurance plan | ✅ comparison + the policies you actually need | partners only |
| Compliance/tax calendar | ✅ `.ics` you import | ❌ |
| Sales-tax nexus & registrations | ✅ | ❌ |
| You own the output & the tool | ✅ Apache-2.0, self-hosted | ❌ SaaS |
| Works offline / your data stays local | ✅ | ❌ |
| Extend / add your own agent | ✅ copy a folder | ❌ |

Keel isn't trying to be a registered agent or file on your behalf — it gets you **all the way to the submit button**, for free, in a tool you own.

## 🚀 Quick Start

```bash
pipx install git+https://github.com/RyanAlberts/ai-native-business-apps.git
keel                      # interactive picker
keel list                 # list every agent
keel founding-journey     # the full Day-0 back office
keel incorporation --cli "Solo founder in Texas, SaaS for plumbers."
```

Prefer to develop locally?

```bash
git clone https://github.com/RyanAlberts/ai-native-business-apps.git
cd ai-native-business-apps && pip install -e .
keel
```

### Auth

If the [Claude Code CLI](https://www.npmjs.com/package/@anthropic-ai/claude-code) is logged into your Claude Max / Pro subscription, you're done — **no API key needed**. Keel's subscription guard recognizes Claude Code / Cursor OAuth markers automatically. For other providers, copy `.env.example` to `.env` and add a key (`OPENAI_API_KEY`, `GOOGLE_API_KEY`, …).

> **💎 On a Max 20x plan?** From **June 15, 2026**, Max 20x subscribers get a separate **$200/mo credit** for Claude Agent SDK usage — *including third-party apps like this one*. Translation: you can run the entire Keel fleet at **$0 marginal cost**, and your interactive Claude Code / chat limits stay untouched. ([details](https://www.claude.com/legal/commercial-terms))

## 📂 The agent fleet

### Starter agents — one task each

Run any with `keel <name>`. Each reads from (and writes to) the shared `company.json`, so the Founding Journey can chain them — or run them solo.

| | Agent | What it does | `name` |
|---|---|---|---|
| 🏛️ | Incorporation | Entity type + state + registered agent + filing checklist. | `incorporation` |
| 📬 | 83(b) Election | 30-day IRS §83(b) letter + postmark deadline + routing + calendar reminder. | `election-83b` |
| 🏛️ | Delaware Franchise Tax | Recompute that $85K bill under both methods — APVC usually lands at $400. | `delaware-franchise-tax` |
| 👥 | Worker Classification | 1099 or W-2? IRS + DOL + state ABC tests with a risk score. | `worker-classification` |
| 📋 | Business License + DBA | Every license/permit/DBA at federal/state/county/city for your industry. | `business-license` |
| 💰 | Loan & Funding | Match SBA / microloan / grant / CDFI programs; prep the package. | `loan` |
| 📜 | Legal Document Generator | Operating agreement, NDA, IP assignment, ToS, contractor agreement. | `legal-doc` |
| 🏦 | Bank & Insurance Setup | Banking comparison + the insurance you actually need. | `bank-insurance` |
| 📋 | Compliance & Tax Setup | Sales-tax nexus, state registrations, annual calendar, bookkeeping. | `compliance-tax` |

### Advanced agents — multi-stage orchestration

| | Agent | Pipeline | `name` |
|---|---|---|---|
| ⚓ | **Founding Journey** ⭐ | Incorporation → 83(b) → Legal → Banking → Compliance → **Day-0 Packet** | `founding-journey` |
| 📋 | Business Plan Manager | Market Research → SWOT → Strategy → 90-day Roadmap | `business-plan` |
| 🌐 | Website Launch Team | Brand → Architecture → Copy → Launch Checklist | `website-launch` |
| 🏭 | Supplier Sourcing Team | Sourcing → Vetting → RFP → Comparison Matrix | `supplier-sourcing` |
| ™️ | Trademark Search Team | Federal ∥ State ∥ Common-Law ∥ Class ID → Verdict + TEAS pre-fill | `trademark-search` |

## 🏗️ Architecture in 30 seconds

```
core/
├── company.py      # the shared Company profile — the spine of the whole product
├── artifacts.py    # prepare-to-submit files: markdown / printable HTML / .ics
├── llm/            # provider abstraction (Claude verified; openai/gemini/xai/ollama)
├── harness/        # Sequential + Parallel orchestration primitives
├── state_portals.py# hand-curated 50-state + federal portal links & fees
├── ui.py           # shared Streamlit UX contract
└── brand.py        # product name in one place

agents/
├── starter_business_agents/   # single-task agents
└── advanced_business_agents/  # multi-agent pipelines (incl. the Founding Journey)
```

Each agent folder is self-contained: `agent.py` (async `run()`), `app.py` (Streamlit), `prompts.py`, `tools.py`, `config.yaml`, `README.md`, `WALKTHROUGH.md`, `PARITY.md`, `tests/golden.jsonl`.

## 💎 Built on the Claude Agent SDK

Every agent is a thin domain layer over [`claude-agent-sdk`](https://docs.claude.com/en/api/agent-sdk) — deliberately **not** LangChain, LangGraph, or a `claude -p` subprocess wrapper. Three reasons:

1. **Predictable billing for Max users.** Agent SDK calls draw on the separate $200/mo SDK credit (from June 15, 2026), making "fork Keel and ship to your own audience" economically viable.
2. **First-class tool routing via MCP.** Our `core.Tool` abstraction wraps tools as `create_sdk_mcp_server` instances — clean structured tool-use, no stdout parsing.
3. **Session isolation.** `ClaudeAgentOptions(setting_sources=[])` runs each agent in a clean session even when launched from inside Claude Code / Cursor.

The provider layer is hand-rolled and lightweight so swapping to OpenAI / Gemini / xAI / local Ollama is one line in `config.yaml`.

## 🔌 Providers

| Provider | Default model | Auth | Status |
|---|---|---|---|
| **claude** | claude-sonnet-4-6 | Claude Max subscription (preferred) or API key | **verified ✅** |
| openai | gpt-4o | API key | working |
| gemini | gemini-2.0-flash | API key | working |
| xai | grok-2-latest | API key | community |
| ollama | llama3.2 | local daemon | community |
| codex | — | ChatGPT sub via Codex CLI | stub (help wanted) |

## 🤝 Contributing

New agents, harnesses, walkthroughs, and provider fixes welcome — every contribution must be hand-built original work, end-to-end tested, and Apache-2.0. See [CONTRIBUTING.md](CONTRIBUTING.md). Good first issues are labeled `good-first-issue`.

## 🙏 Credits

Built by [Ryan Alberts](https://github.com/RyanAlberts), with structural inspiration from [`awesome-llm-apps`](https://github.com/Shubhamsaboo/awesome-llm-apps) (see [NOTICE](NOTICE)). No code or prompts are copied from upstream — every agent here is original work.

## ⭐ Star History

If Keel saved you a weekend of back-office grind, a star helps other founders find it.
