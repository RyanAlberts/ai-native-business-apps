# 🌐 Website Launch Team

> Sequential 4-stage pipeline — Brand → Architecture → Copy → Launch
> checklist — that takes a business idea and produces a complete site
> launch plan you can execute in 14 days.

## Pipeline

| # | Stage | Output |
|---|---|---|
| 1 | **Brand & Domain** | Name (+3 alternates), `.com` strategy, brand voice, color palette, fonts, logo concept, positioning sentence. |
| 2 | **Site Architecture** | Sitemap, page-by-page outlines, reusable components, conversion path, tech stack pick. |
| 3 | **Copy & Design Direction** | Hero copy + CTA, problem/solution copy, feature blocks, social-proof placeholders, pricing copy, design direction. |
| 4 | **Launch Checklist** | Pre-launch tasks (-14 to -1), Day 0 ops, Days 1–14 monitoring, marketing handoff, success metrics. |

Each stage's output feeds the next — the launch checklist references the
specific tech stack the architect picked and the specific copy the
copywriter wrote.

## Run

```bash
agent website-launch
agent website-launch --cli "AI hiring screener for SaaS recruiting teams. Bootstrapped, $30k budget, ship in 14 days."
```

Pipeline runtime: ~8–10 minutes end-to-end on `claude-sonnet-4-6`
(per-stage ~120–140s × 4 stages, verified 2026-05-14). Set client
timeouts ≥ 600s when scripting against this agent. Pass an
`on_stage_complete` callback to stream per-stage progress to your UI.

## Customize

- Add a stage (e.g. *SEO Strategy*) by appending a `Stage` to
  `_stages()` in `agent.py` and a new prompt to `prompts.py`.
- Drop a stage you don't need (e.g. skip "Copy" if you've already written
  it).
- Re-order stages — though brand → architecture → copy → checklist is the
  natural order.

## Provider parity

Verified on Claude. Multi-stage works on all providers; quality of
brand/naming is best on Claude due to depth of training data on naming.
See [PARITY.md](./PARITY.md).
