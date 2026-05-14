# Business Idea Validator (template)

> The canonical example of building an agent on the
> [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk). Copy this
> folder, edit five files, ship a new agent.

The example agent itself validates a startup idea — takes one paragraph
in, returns a structured markdown analysis (problem, target customer,
MVP scope, top risks, first experiment). But the real point of this
folder is to demonstrate the **agent-building pattern** so you can fork
it for any business task.

## The Agent SDK pattern

Every agent in this repo is built on `claude-agent-sdk` for three
concrete reasons (the full case is in the root [README](../README.md#-built-on-claude-agent-sdk)):

1. **Max 20x billing.** Post-June 15, 2026, Agent SDK calls draw on a
   separate $200/mo credit, not the interactive Claude Code / chat cap.
2. **MCP tool routing.** The SDK speaks MCP natively, so custom tools
   become first-class structured tool-use messages instead of stdout to
   parse.
3. **Session isolation.** `setting_sources=[]` keeps each agent run
   reproducible regardless of the host's installed skills/plugins.

The shape is always the same:

```python
# agent.py
from core import get_llm, load_config
from .prompts import SYSTEM_PROMPT
from .tools import all_tools

async def run(user_input: str) -> str:
    config = load_config(__file__)
    llm = get_llm(config)                     # ClaudeClient by default
    return await llm.complete(
        system_prompt=SYSTEM_PROMPT,
        user_message=user_input,
        tools=all_tools(),
    )
```

Under the hood, `ClaudeClient.complete()` constructs
`ClaudeAgentOptions(model=..., system_prompt=..., mcp_servers=...,
allowed_tools=..., setting_sources=[])` and iterates the SDK's
`query(prompt=..., options=...)` async generator until the final
`ResultMessage` arrives. The SDK handles the tool loop, MCP routing,
and OAuth detection automatically. We never touch it directly.

## Run this template

```bash
# From the repo root, with claude-agent-sdk installed (pip install -e .)
unset ANTHROPIC_API_KEY                      # use Claude Max subscription
streamlit run _template/app.py
```

CLI:
```bash
python -m _template.agent "A subscription box for office snacks"
```

Or via the `agent` launcher (if installed via pipx):
```bash
agent --cli "A subscription box for office snacks"
```

## Copy this template → ship a new agent

1. **Copy** the entire `_template/` folder to
   `starter_business_agents/<your_agent>/` (single-agent) or
   `advanced_business_agents/multi_agent_apps/<your_team>/` (multi-stage).
2. **Edit `prompts.py::SYSTEM_PROMPT`** — change the role and output
   format. This is where 90% of the agent's behavior lives.
3. **Edit `tools.py::all_tools()`** — return `core.Tool` instances for
   any custom capabilities. The Agent SDK wraps them as MCP servers.
4. **Edit `config.yaml`** — pick a provider/model, set
   `allowed_tools` (Claude built-ins like `WebSearch`), declare external
   MCP servers if you need them.
5. **Edit `agent.py::run()`** — update the function signature, type
   hints, and docstring. The body usually stays as-is.
6. **Rewrite this README + WALKTHROUGH.md + PARITY.md** for your agent's
   purpose.

## File layout (every agent follows this)

```
<your_agent>/
├── agent.py            # async def run() — the SDK call
├── app.py              # Streamlit UI wrapper
├── prompts.py          # SYSTEM_PROMPT (named constants)
├── tools.py            # all_tools() -> list[core.Tool]
├── config.yaml         # provider, model, MCP servers, allowed_tools
├── requirements.txt    # only if extra deps beyond root
├── README.md           # this file, for your agent
├── WALKTHROUGH.md      # narrative tutorial
├── PARITY.md           # provider-by-provider verification status
└── tests/
    ├── golden.jsonl    # 3–5 canonical prompts
    └── baselines/      # frozen captures for diffing
```

## Multi-stage agents

For pipelines (Market Research → SWOT → Strategy → Roadmap), build the
same `agent.py` but using
[`core.SequentialHarness`](../core/harness/sequential_harness.py) — each
`Stage` makes its own SDK call and pipes output forward. See
`advanced_business_agents/multi_agent_apps/business_plan_implementation_manager/`
for a working example.

## Provider parity

See [PARITY.md](./PARITY.md). Verified on Claude (subscription /
Agent SDK credit). OpenAI/Gemini work; xAI/Ollama community-supported;
Codex stub.

## Model

Claude Sonnet 4.6 by default. Override per-environment with
`CLAUDE_MODEL=…`, or globally in `config.yaml`.
