# Business Idea Validator (template)

A reference single-agent template you can copy into `starter_business_agents/`
or `advanced_business_agents/` to start a new agent. Demonstrates the
provider-agnostic agent contract end-to-end.

## What it does

Takes a one-paragraph business idea and returns a structured markdown analysis
covering the problem, target customer, MVP scope, top risks, and a concrete
first experiment.

## Run

```bash
# From the repo root, with claude-agent-sdk installed (pip install -e .)
unset ANTHROPIC_API_KEY                      # use Claude Max subscription
streamlit run _template/app.py
```

CLI:
```bash
python -m _template.agent "A subscription box for office snacks"
```

## Customize

This template is meant to be copied. To turn it into your own agent:

1. Copy the entire `_template/` folder to `starter_business_agents/NN_<your_agent>/`.
2. Edit `prompts.py::SYSTEM_PROMPT` — change the role and output format.
3. Edit `tools.py::all_tools()` — return any `Tool` objects you need.
4. Edit `config.yaml` — pick a provider/model.
5. Update `agent.py::run()`'s signature and docstring.
6. Rewrite this README.

## Provider parity

See [PARITY.md](./PARITY.md). Verified on Claude (subscription). OpenAI/Gemini
work; xAI/Ollama community-supported; Codex stub.

## Model

Claude Sonnet 4.6 by default. Override per-environment with `CLAUDE_MODEL=...`,
or globally in `config.yaml`.
