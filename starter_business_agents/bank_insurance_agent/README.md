# 🏦 Bank & Insurance Setup Agent

> Pick a business bank, figure out which insurance you actually need, and
> get a 30-day action plan. No upsells.

## What it does

Takes a business profile (state, stage, employees, physical space, data
sensitivity, services offered) and returns:

- **Banking:** one recommended bank + 3-option comparison table + docs
  checklist + common pitfalls
- **Insurance:** ranked list of policies this founder needs (GL, E&O,
  cyber, workers' comp, BOP, etc.) with coverage limits, cost ranges, and
  why each one matters for THIS business
- **Carriers/brokers** to get quotes from
- **First-year cost summary** (banking + insurance combined)
- **30-day action plan**

## Run

```bash
agent bank-insurance
agent bank-insurance --cli "Two-person LLC, software consulting for clinics in CA, $200k revenue, no PHI stored, no physical office."
```

## Why this matters

Most founders pick a bank because of a billboard and skip insurance until
their first claim. This agent forces the right ordering: bank first
(can't deposit checks without it), then GL/E&O (your first real risk
exposure), then state-required (workers' comp the day you hire), then
nice-to-have.

## Customize

- **Add a banking option** (e.g. a local credit union you trust) — edit
  the comparison-table section in `prompts.py::SYSTEM_PROMPT`.
- **Industry-specific insurance** — add rules like *"If business is in
  food service, require product liability and recommend Inn-General
  carriers."* to the prompt.

## Provider parity

Verified on Claude (subscription). See [PARITY.md](./PARITY.md).
