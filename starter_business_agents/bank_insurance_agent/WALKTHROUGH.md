# Walkthrough — Bank & Insurance Setup Agent

> "I just incorporated. What bank should I use, and what insurance do I
> actually need vs. what brokers are going to try to sell me?"

This agent gives the founder a defensible answer to both questions in 60
seconds — including which policies to skip.

## What you'll see

Run `agent bank-insurance` and fill the form for a 2-person CA consulting LLC
serving healthcare clinics with no PHI. You get:

1. **Recommendation summary** — typically "Mercury for banking + GL/E&O/Cyber
   as core insurance" or similar, sized to the business.
2. **Banking section** — one primary recommendation, comparison table of 3,
   docs checklist (EIN letter, articles, operating agreement, ID, initial
   deposit), banking pitfalls (commingling funds, FDIC at fintechs, etc.).
3. **Insurance section** — ranked policies (GL, E&O, Cyber for this profile),
   each with coverage limits, cost ranges, and "why this founder."
4. **Carriers** — Hiscox, Next, Thimble, or a local independent broker
   depending on complexity.
5. **First-year cost summary** — adds it all up.
6. **30-day plan** — bank → quotes → bind → state-required.

## How it works

One LLM call, temperature 0.2. The prompt is structured so the LLM must
rank insurance by necessity (not include everything), which prevents the
common "broker upsell" output style.

## Customizing it

### Bias toward a specific bank you love

Edit `prompts.py::SYSTEM_PROMPT`. In the "Recommended account" section,
change *"Pick ONE primary option"* to *"Strongly prefer Mercury unless
the founder needs in-person banking, in which case Chase."* The agent
will follow the bias.

### Add industry-specific insurance rules

The prompt currently lets the LLM infer. If your fork is for a specific
vertical (e.g. food trucks), hard-code: *"If business serves food, ALWAYS
include Product Liability and Spoilage coverage."*

### Use OpenAI for variety

```yaml
provider: openai
model: gpt-4o
temperature: 0.2
```

## Going further

- Pair with the [**Incorporation Agent**](../incorporation_agent/) —
  banks require the operating agreement; this one tells you what to bring.
- Pair with the [**Compliance & Tax Setup Agent**](../compliance_tax_agent/) —
  the workers' comp + state filings sit at the intersection of both.

## Footer

From **AI-Native Business Apps** — hand-built, provider-agnostic, Apache-2.0.
