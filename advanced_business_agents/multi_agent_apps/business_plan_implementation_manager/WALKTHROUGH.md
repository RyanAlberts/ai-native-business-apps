# Walkthrough — Business Plan Implementation Manager

> "I have a business idea. What do I do for the next 90 days?"

This agent answers that question — but not as a generic business plan dumped
out of a single LLM call. It runs a **4-stage sequential pipeline** so each
piece of strategic reasoning builds on the prior step's output, the way a
real strategy consultant would.

## What you'll see

Paste this idea into the app:

> *I'm a former enterprise SaaS sales rep. I want to build a vertical CRM
> specifically for independent insurance brokers. Target market: the ~36k US
> brokerages with 2–10 employees. I have $50k savings to fund 6 months of
> focused work.*

The agent walks through four stages over ~2 minutes (you can watch each one
expand as it completes):

1. **Market Research** — *the agent uses WebSearch to verify current market
   data.* You get a structured brief covering:
   - Market overview (insurance agency management software, ~$X billion)
   - Real competitor names (AgencyZoom, HawkSoft, Vertafore, EZLynx, etc.)
   - Pricing landscape ($X/seat/mo typical)
   - Recent shifts (Vertafore acquisition of AgencyZoom, etc.)
2. **SWOT Analysis** — quadrants grounded in the brief. Real items, not
   "Strength: passionate team."
3. **Strategy** — picks ONE beachhead segment (e.g. "HawkSoft agencies"), ONE
   acquisition channel, names what you're NOT doing.
4. **Implementation Roadmap** — concrete 30/60/90-day deliverables with
   acceptance criteria ("Build 200-agency HawkSoft prospect list — acceptance:
   spreadsheet with confirmed AMS + commercial-lines indicators; effort ~16
   hrs"), key metrics dashboard, and critical decision forks.

The output isn't a slide deck. It's an execution plan a solo founder can
start working through on day 1.

## How it works

```
┌──────────────────────────────────────────────────────────────────────┐
│                       SequentialHarness                              │
│                                                                      │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│   │ Stage 1  │───>│ Stage 2  │───>│ Stage 3  │───>│ Stage 4  │      │
│   │ Market   │    │  SWOT    │    │ Strategy │    │ Roadmap  │      │
│   │ Research │    │ Analysis │    │          │    │          │      │
│   │ +Web     │    │          │    │          │    │          │      │
│   │ Search   │    │          │    │          │    │          │      │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘      │
│        │              │              │              │               │
│        └──────────────┴──────────────┴──────────────┘               │
│                   (output of N = input of N+1)                       │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
                              │
                              v
                       ┌──────────────┐
                       │  LLM Client  │
                       │  Claude Max  │
                       └──────────────┘
```

Three files do the work:

- **`agent.py`** wires the four `Stage` objects to a `SequentialHarness` and
  runs it.
- **`prompts.py`** has the four system prompts — one per stage. Each prompt
  expects to read the prior stage's output as data.
- **`config.yaml`** sets the model, temperature, and `allowed_tools:
  [WebSearch]` so stage 1 can verify market data.

The `SequentialHarness` itself lives in [`core/harness/sequential_harness.py`](../../../core/harness/sequential_harness.py).
It's ~50 lines. Read it — it's small enough to fully understand.

## Customizing it

### Swap a stage's prompt

Open `prompts.py`. Edit `STRATEGY_PROMPT` to make it more or less aggressive,
or to enforce a different output structure. No code changes needed.

### Add a stage

In `agent.py::_stages()`, append a new `Stage`:

```python
Stage(
    name="Fundraising Prep",
    system_prompt=FUNDRAISING_PROMPT,  # add this in prompts.py
    input_template="Roadmap:\n\n{input}",
),
```

The harness will now run 5 stages. The new one receives the roadmap as input.

### Remove the web-search dependency

For provider agnosticism, comment out `WebSearch` in `config.yaml`:

```yaml
allowed_tools: []
```

The model still produces a research brief from training data — slightly less
current but still useful.

### Change the orchestration pattern

`SequentialHarness` is one pattern. For fan-out + merge, write a
`ParallelHarness` (planned for v1.1): each stage runs concurrently, results
merged in a final synthesis call. The `core/harness/` directory is
deliberately tiny so you can copy `sequential_harness.py` and modify it.

## Why this beats a single LLM call

If you prompt one LLM with "make me a business plan for an insurance broker
CRM," you get *generic* output. Pipeline this and:

- Stage 1 grounds the rest in real market data (web-search'd).
- Stage 2 forces the LLM to actually engage with that data before drafting
  strategy.
- Stage 3 makes hard tradeoffs (one channel, one segment, one price) instead
  of giving you a buffet.
- Stage 4 converts those tradeoffs into action items, not abstractions.

The total context grows across stages, so by stage 4 the LLM has seen the
market reality, the SWOT, AND the strategic commitments. It can't fall back
on generic advice.

## Going further

- Run the [**Incorporation Agent**](../../../starter_business_agents/incorporation_agent/) after this — once you have a strategy, the entity decisions are more obvious.
- Add a `web_search` tool to `tools.py` to bring full market research parity
  to OpenAI / Gemini / Ollama. See `_template/tools.py` for the pattern.
- Build your own `ParallelHarness` for use cases like multi-perspective due
  diligence (legal + financial + competitive in parallel, synthesized at the
  end).

## Footer

From **AI-Native Business Apps** — hand-built, provider-agnostic, Apache-2.0.
The sequential pattern in this agent is inspired by Google ADK's
[`SequentialAgent`](https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/ai_agent_framework_crash_course/google_adk_crash_course/9_multi_agent_patterns/9_1_sequential_agent),
rebuilt provider-agnostically. None of the upstream code or prompts are used.
