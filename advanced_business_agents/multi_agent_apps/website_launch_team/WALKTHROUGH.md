# Walkthrough — Website Launch Team

> "I have an MVP. I need a website to start sending traffic to. Where do I
> even begin — what do I name it, what do I put on the homepage, what
> platform, what goes on launch day?"

This agent answers all of that in a single 2-minute run.

## What you'll see

Run `agent website-launch --cli "AI hiring screener for SaaS recruiting teams, $30k budget, live in 14 days"`. You'll watch four stages execute in sequence:

1. **Brand & Domain** — Returns a primary name + 3 alternates with `.com`
   availability strategy, a positioning sentence, a color palette
   (with HEX codes), font recommendations, and a one-paragraph logo
   concept.
2. **Site Architecture** — Reads the brand output, then picks a site type
   (usually "marketing site, 5–8 pages" for this profile), gives a nested
   sitemap, page-by-page outlines, reusable components, conversion path,
   and a tech stack pick (Framer / Next.js+Vercel / Wordpress / Shopify).
3. **Copy & Design Direction** — Writes actual hero copy (headline,
   subheadline, CTA), problem/solution sections, 3–6 feature blocks with
   value statements, design direction.
4. **Launch Checklist** — Concrete pre-launch (DNS, hosting, QA, legal
   pages, analytics), Day 0 ops, Days 1–14 monitoring, marketing handoff,
   30-day success metrics.

The final checklist is grounded in the actual brand, architecture, and
copy — not generic launch advice.

## How it works

Uses `core.SequentialHarness` with 4 stages. Each stage uses its own
system prompt and inherits the prior stage's output as input. Same pattern
as `business_plan_implementation_manager`.

## Customizing it

### Bias toward a tech stack

Edit `prompts.py::SITE_ARCHITECTURE_PROMPT`. Replace the tech stack
section with a hard preference: *"Always recommend Framer for non-technical
founders, Next.js + Vercel for technical founders, no other options."*

### Change the voice

The copy stage tends toward "confident, founder-voice." If you want more
playful or more enterprise-y, edit `COPY_DESIGN_PROMPT`'s tone instruction.

### Skip a stage

In `agent.py::_stages()`, comment out the stage you don't need. The
harness handles any number of stages.

## Going further

- Pair with the [**Business Plan Implementation Manager**](../business_plan_implementation_manager/)
  — run that first to define strategy and positioning; this agent builds
  the website around it.
- Pair with the [**Legal Doc Generator**](../../../starter_business_agents/legal_doc_agent/)
  for ToS and Privacy Policy (mentioned in the launch checklist).

## Footer

From **AI-Native Business Apps** — hand-built, provider-agnostic, Apache-2.0.
