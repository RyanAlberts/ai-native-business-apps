# Walkthrough — Founding Journey

This is the agent that turns a pile of single-purpose tools into a
product. Here's how it works, end to end.

## 1. One profile, not twelve forms

Every standalone agent asks for the same facts — company name, state,
entity type, funding stage. The journey collects them once into a
[`Company`](../../../core/company.py) dataclass:

```python
from core import Company, Founder

company = Company(
    legal_name="Northwind Robotics, Inc.",
    one_liner="Warehouse picking robots for mid-size 3PLs",
    home_state="California",
    state_of_formation="Delaware",
    entity_type="C-Corp",
    formation_date="2026-06-01",
    funding_stage="Priced seed (9–18 months)",
)
```

`Company.to_context()` renders this into a compact block that's prepended
to every step's prompt, so no specialist re-asks for it.

## 2. The pipeline, in real-world order

`run_journey()` walks the [`default_steps()`](journey.py) — incorporation,
83(b), legal docs, banking & insurance, compliance & tax — driving each
with a single shared `LLMClient`. Crucially, it threads a running
transcript forward: step 3 (legal docs) sees the entity type step 1 chose,
so the operating agreement matches the structure.

```python
from advanced_business_agents.multi_agent_apps.founding_journey.journey import run_journey

result = await run_journey(company, on_step=lambda s: print("done:", s.title))
```

## 3. Synthesis

After the five specialists run, a coordinator prompt reconciles their
outputs into one **Day-0 Formation Packet**: a single ordered checklist
(you can't get an EIN before the entity exists; you can't open a bank
account before the EIN), a deadlines table, a deduplicated link index, and
a list of documents prepared.

## 4. Prepare-to-submit artifacts

`result.artifacts()` returns an `ArtifactSet`:

```python
for art in result.artifacts():
    print(art.filename, "—", art.label)
# company.json — Company profile
# 00-formation-packet.md — Day-0 Formation Packet (Markdown)
# 00-formation-packet.html — printable / Save-as-PDF
# 01-incorporation.md … 05-compliance_tax.md
# compliance-deadlines.ics — import to your calendar
```

The `.ics` is built from `deadlines_for(company)`, which computes dates
**deterministically** (83(b) = formation date + 30 days; DE franchise tax
= next March 1). LLM text is never parsed into calendar entries.

## 5. Test it offline

Because the journey takes an injectable `llm`, the entire flow is tested
with a `FakeLLM` — no network, no Claude auth — verifying step order,
context threading, synthesis, and artifact generation. Run:

```bash
pytest advanced_business_agents/multi_agent_apps/founding_journey/tests -q
```

## Customize

- **Reorder or swap steps:** edit `default_steps()` or pass your own
  `steps=` list to `run_journey()`.
- **Add a step:** import another agent's `SYSTEM_PROMPT` + `all_tools` and
  append a `JourneyStep`.
- **Change deadline logic:** extend `deadlines_for()`.
