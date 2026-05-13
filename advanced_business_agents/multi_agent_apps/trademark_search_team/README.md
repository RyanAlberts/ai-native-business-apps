# Trademark Search Team

**What LegalZoom charges**:
- Federal search: **$199**
- Comprehensive search (federal + state + common-law): **$299**
- Registration package: **$899** + USPTO fees
- Trademark "bait-and-switch" complaint pattern: founders pay $649 only
  to be told the comprehensive search isn't included after they've
  already committed.

**What a trademark attorney charges** for a pre-filing review: **$500–$1,500**.

**What this agent charges**: **$0**. (USPTO filing fee still goes to USPTO.)

## The architectural showcase

This is the repo's first agent that uses **`ParallelHarness`** — four
research sub-agents run **concurrently** against the same proposed
mark, then a synthesizer consolidates their findings into a single
decision-quality report.

```
                    ┌──────────────────┐
                    │  Federal TESS    │──┐
                    │  (USPTO)         │  │
                    └──────────────────┘  │
                    ┌──────────────────┐  │   ┌─────────────┐
   Proposed mark ──▶│  State SoS       │──┼──▶│ Synthesizer │──▶ Verdict
   + goods/svcs     │  registries      │  │   │ + TEAS      │    + TEAS
                    └──────────────────┘  │   │ pre-fill    │    pre-fill
                    ┌──────────────────┐  │   │ + fee est   │    + fee
                    │  Common-law      │──┤   └─────────────┘
                    │  conflict scan   │  │
                    └──────────────────┘  │
                    ┌──────────────────┐  │
                    │  USPTO class     │──┘
                    │  identification  │
                    └──────────────────┘
                    (each uses WebSearch)
```

The branches are independent — no branch waits on another. The
synthesizer runs after all four return.

## Outputs

The synthesizer produces:

1. **Verdict**: GO / CAUTION / NO-GO with a 2–3 sentence rationale.
2. **Conflicts ranked by severity** — a table citing source URLs.
3. **Recommended USPTO class(es)** with descriptions (verbatim from the
   ID Manual where TEAS Plus-eligible).
4. **Filing fee estimate** — from the deterministic `uspto_fee_estimate`
   tool. Line-by-line breakdown + maintenance fees at year 6 and 10.
5. **TEAS application pre-fill** — values the founder can paste into
   the USPTO TEAS Plus form, with `[FOUNDER]` placeholders for fields
   the agent should never fill in (TIN, applicant name, signature).
6. **Calendar deadlines** — Office Action response windows, Statement
   of Use deadlines, Section 8 maintenance, Section 9 renewal.
7. **Next steps** — verify on uspto.gov, file at teas.uspto.gov,
   calendar deadlines.
8. **Disclaimer**.

## Quick start

```bash
# CLI
python -m advanced_business_agents.multi_agent_apps.trademark_search_team.agent \
  "Proposed mark: 'BLUEHORSE'. Goods/services: AI-powered photo editing \
   software for mobile devices. Founder is a CA LLC. Intent-to-use."

# Streamlit UI
streamlit run advanced_business_agents/multi_agent_apps/trademark_search_team/app.py
```

## Architecture details

- Built on **`core.ParallelHarness`** (this repo's fan-out-then-synthesize
  primitive). The same harness can be reused for any future multi-research
  agent — e.g. supplier due diligence, competitor analysis, due-diligence
  background checks.
- Each branch is just a `Stage` with its own system prompt. Adding a
  fifth branch (e.g. EU trademarks via EUIPO) is a one-line change.
- The synthesizer has access to one deterministic tool —
  `uspto_fee_estimate` — so the fee math is never LLM-fabricated.
- Provider-agnostic: the YAML config picks Claude by default, but
  swapping `provider: openai` would work too if the openai SDK is
  installed and `OPENAI_API_KEY` is set.

## Critical: WebSearch is required

The branches NEED real web access to pull current TESS records, state
SoS data, and common-law evidence. Without WebSearch, the agent will
hallucinate trademark records — and that's worse than no findings at
all. The default `config.yaml` enables WebSearch via the Claude
provider's built-in tools.

If you swap to a provider that doesn't have a built-in WebSearch tool,
either:
- Add an MCP search server in `mcp_servers:` in the config, or
- Add a custom web-search Tool in `tools.py` (e.g. a Brave Search API
  wrapper).

## NOT legal advice

Trademark conflicts are fact-intensive. The §2(d) likelihood-of-confusion
examination is subjective and the USPTO examining attorney has wide
discretion. A CAUTION or NO-GO verdict in particular warrants attorney
review — the $250–$350 filing fee per class is non-refundable on refusal,
and a refused application is in the public record.

The agent's output is research + draft, not a filed application.

## Sources

- USPTO TESS: https://tmsearch.uspto.gov/
- USPTO ID Manual (Nice Classification): https://idm-tmng.uspto.gov/
- USPTO Fee Schedule: https://www.uspto.gov/trademarks/fees-payment-information
- TEAS filing portal: https://teas.uspto.gov/
- Nice Classification (15-12-2025 edition): https://www.wipo.int/classifications/nice/
