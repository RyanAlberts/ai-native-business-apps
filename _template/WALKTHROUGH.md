# Walkthrough — Building Your First AI-Native Business Agent

You just cloned an open-source repo of business agents and you want to ship
your own version. This walkthrough takes you from `git clone` to a customized,
running agent in about 15 minutes.

## What you'll build

A single-agent Streamlit app that validates startup ideas. By the end, you'll
have an agent that takes any business idea as input and returns a structured
analysis — problem, target customer, MVP scope, top risks, and a first
experiment to run this week.

## How it works (90 seconds)

The template is three pieces glued together:

```
   ┌─────────────┐     ┌─────────────┐     ┌──────────────┐
   │  app.py     │ ──> │  agent.py   │ ──> │  core/llm/   │
   │  Streamlit  │     │ run(idea)   │     │  provider    │
   └─────────────┘     └─────────────┘     └──────────────┘
                              │                    │
                              v                    v
                      ┌─────────────┐      ┌──────────────┐
                      │  prompts.py │      │  config.yaml │
                      │  tools.py   │      │  provider:   │
                      └─────────────┘      │  claude      │
                                           └──────────────┘
```

- `app.py` is the Streamlit UI.
- `agent.py::run()` is the importable async entry point. It loads
  `config.yaml`, builds an LLM client, and runs one completion.
- `core/llm/` is the provider abstraction. Swap `claude` → `openai` in
  `config.yaml` and the same code runs against OpenAI.

## Customizing the agent

Three knobs cover ~90% of customizations.

### 1. Change the role (`prompts.py`)

Open `prompts.py` and replace `SYSTEM_PROMPT`. For example, to turn this
into a "Cofounder Matcher Agent":

```python
SYSTEM_PROMPT = """\
You evaluate whether two prospective cofounders should team up. Given a
description of both founders' skills, motivations, and life situation,
return a markdown report with sections: Compatibility (1-10), Strengths,
Gaps, Red Flags, Recommended Next Step.
"""
```

### 2. Change the provider (`config.yaml`)

```yaml
provider: openai           # was: claude
model: gpt-4o              # was: claude-sonnet-4-6
auth_mode: api_key         # OpenAI is API-only
```

Set `OPENAI_API_KEY` in your `.env` and you're done. Same code, different
provider.

### 3. Add a tool (`tools.py`)

If you want the LLM to call out to the web, the filesystem, or an external
API, define a `Tool`:

```python
from core import Tool

async def _domain_lookup(args: dict) -> str:
    import subprocess
    return subprocess.check_output(["whois", args["domain"]]).decode()

DOMAIN_LOOKUP = Tool(
    name="domain_lookup",
    description="Look up WHOIS info for a domain.",
    input_schema={
        "type": "object",
        "properties": {"domain": {"type": "string"}},
        "required": ["domain"],
    },
    handler=_domain_lookup,
)

def all_tools():
    return [DOMAIN_LOOKUP]
```

The agent can now call `domain_lookup` whenever the prompt prompts it to.

## Going further

- **Multi-stage agents** — check out
  `advanced_business_agents/multi_agent_apps/business_plan_implementation_manager/`
  for a sequential 4-stage pipeline using `SequentialHarness`.
- **External tools via MCP** — wire Firecrawl, Tavily, or Composio in
  `config.yaml::mcp_servers`. No Python changes needed.
- **Custom orchestration patterns** — see `core/harness/` to build your
  own `ParallelHarness` or `LoopHarness`.
- **Contribute** — your agent could be the next one featured in the README.
  See `CONTRIBUTING.md`.

## Footer

This is a walkthrough from **AI-Native Business Apps**, a hand-built,
provider-agnostic, Apache-2.0 toolkit for founders who want AI baked in
from day 0.
