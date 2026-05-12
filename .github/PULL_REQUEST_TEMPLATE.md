<!--
Thanks for the PR! Please fill out the checklist so reviewers can land it
quickly. See CONTRIBUTING.md for the full standard.
-->

## What this PR does
<!-- 1-3 sentences. Lead with the founder outcome, not the code. -->

## Scope
- [ ] New agent (specify path):
- [ ] New harness / provider / skill:
- [ ] Bug fix:
- [ ] Docs / walkthrough:
- [ ] Refactor / cleanup:

## Checklist (for new agents)

- [ ] Folder follows `_template/` shape (`agent.py`, `app.py`, `prompts.py`, `tools.py`, `config.yaml`, `README.md`, `WALKTHROUGH.md`, `PARITY.md`, `tests/golden.jsonl`).
- [ ] `agent.py::run` is `async def` and importable.
- [ ] No `import openai` / `import anthropic` / framework deps in agent code — all LLM calls go through `core.get_llm`.
- [ ] Prompts live in `prompts.py` as named constants.
- [ ] Apache-2.0 header at the top of every new Python file.
- [ ] `tests/golden.jsonl` has at least 3 prompts.
- [ ] `PARITY.md` reflects what was actually run (`verified` for Claude, `working` / `community-supported` honestly for others).
- [ ] Added to the README's agent listing.

## How I tested
<!-- Concrete commands you ran. The reviewer will run them too. -->

```
python -m <your_module>.agent "your test input"
```

## Anything reviewers should pay extra attention to?
