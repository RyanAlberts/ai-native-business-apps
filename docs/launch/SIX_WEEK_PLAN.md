# Keel — 6-Week Launch Plan

Goal: go from **0 stars → meaningful traction** (target: 1,000+ GitHub
stars, a front-page Hacker News / Product Hunt moment, and a self-sustaining
contributor trickle) in six weeks.

The strategy is **"one undeniable demo + relentless distribution."** The
product's wedge is the [Founding Journey](../../advanced_business_agents/multi_agent_apps/founding_journey/):
*fill in your company once, download a complete Day-0 formation packet for
free.* Every piece of content points back to that 90-second wow.

---

## The positioning (say this everywhere, identically)

> **Keel — the open-source alternative to Stripe Atlas.** Incorporate, bank,
> and stay compliant from Day 0, running on the Claude subscription you
> already pay for. No API key, no SaaS bill, you own all of it.

Three hooks, ranked by tested resonance:
1. **"Open-source Stripe Atlas"** — instant comprehension, strong search intent.
2. **"$0 instead of $500, and you own it"** — the founder's wallet.
3. **"It hands you the actual files, ready to file"** — the believability gap competitors leave open.

---

## Pre-launch (Week 0 — before any announcement)

This is the difference between a launch that sticks and one that 404s on
arrival. **Do not announce until all of these are true.**

- [ ] **The demo is real.** A 60–90s screen recording of `keel founding-journey`: intake → live progress → packet → downloading `00-formation-packet.html` and the `.ics`. This GIF goes in the README hero and every post.
- [ ] **The README's first screen sells in 10 seconds** (done — verify the hero GIF renders on github.com, not just locally).
- [ ] **One-command install actually works** on a clean machine (test `pipx install git+…` in a fresh VM/container).
- [ ] **CI is green and visible** (badge in README). Trust signal.
- [ ] **5–8 `good-first-issue`s filed** so the first wave of interested devs have an on-ramp (e.g. "add WA/OR sales-tax rules", "port Codex provider", "add EIN-prep artifact").
- [ ] **`CONTRIBUTING.md` + issue templates** polished (already present).
- [ ] **GitHub Discussions on**, with a pinned "Show us what you incorporated" thread.
- [ ] **Social proof seeds:** get 5–10 founder friends to actually run it and star it the morning of launch (cold repos with 0 stars die on HN).
- [ ] **A landing page** (GitHub Pages is fine) at a memorable URL, or at minimum a clean repo social-preview image.

---

## Week 1 — The Hacker News / "Show HN" beat

HN is the single highest-leverage launch surface for a dev-facing open-source tool.

- **Tue–Thu, 8–10am ET** is the sweet spot. Title: `Show HN: Keel – open-source AI back-office for founders (alt to Stripe Atlas)`.
- Post the [Show HN draft](SHOW_HN.md). First comment from you = the "why I built this" story + the honest limitations (this earns trust and preempts the top critical comment).
- **Be present for 6 straight hours** replying to every comment. Engagement velocity in hour 1–2 determines front-page survival.
- Cross-post to **r/startups, r/Entrepreneur, r/ycombinator, r/SideProject** (stagger across the week; each subreddit hates seeing the same post elsewhere same-day).
- Submit to **Lobsters** if you have an invite.

**Success metric:** HN front page (top 30) for 3+ hours → typically 300–800 stars in 48h.

---

## Week 2 — Product Hunt + the founder-Twitter/X engine

- **Product Hunt launch** (Tue or Wed, 12:01am PT). Use the [PH draft](PRODUCT_HUNT.md). Line up 15–20 supporters to comment (not just upvote — PH weights comments). Offer a "first 100 founders get a custom agent built" hook.
- **X/Twitter thread** ([draft](LAUNCH_THREAD.md)) timed to the PH launch. The thread *is* the demo — GIF in tweet 1, the vs-Atlas table as an image in tweet 3.
- Tag/DM founder-audience accounts who riff on "AI for founders" and Stripe Atlas alternatives. Ask for a quote-tweet, not a favor.
- Post the same thread on **LinkedIn** (different audience: operators, fractional execs, accelerator staff).

---

## Week 3 — Long-tail SEO + the "comparison" content play

People Google "Stripe Atlas alternative", "how to file 83(b)", "Delaware franchise tax too high". Own those queries.

- Publish 3 deep, genuinely-useful posts (dev.to / Hashnode / your blog), each ending in a Keel CTA:
  1. *"I rebuilt Stripe Atlas as an open-source AI agent — here's the architecture"* (HN/dev crowd).
  2. *"The $85K Delaware franchise tax bill is a bug, not a fact"* (founder pain, links the franchise-tax agent).
  3. *"Miss the 83(b) 30-day window and you can't undo it. Here's an agent that won't let you."* (urgency).
- Turn each agent's `WALKTHROUGH.md` into a standalone tutorial.
- Submit the architecture post to HN as a separate `Show HN`/blog link (different angle, fair game).

---

## Week 4 — Distribution partnerships

- Get listed in **awesome-lists**: `awesome-claude`, `awesome-agents`, `awesome-llm-apps` (the inspiration repo — open a PR adding Keel), `awesome-selfhosted`.
- Pitch **accelerators / founder communities** (YC Startup School, Indie Hackers, On Deck, local startup Slacks): "free, open-source Day-0 toolkit for your batch."
- Reach out to **Anthropic devrel** — Keel is a flagship example of an app built on the Agent SDK + the Max SDK-credit story. A retweet or a docs mention is rocket fuel.
- Offer a **5-minute conference-talk / podcast** version of the architecture story.

---

## Week 5 — Community flywheel

- Triage and merge the first external PRs **fast** (a merged PR in <24h converts a contributor for life).
- Ship a visible **v0.2** with 1–2 community-requested agents and a CHANGELOG. "It's alive and moving" retains stars.
- Run a **"add your state" sprint** — the 50-state data is the most parallelizable contribution surface; turn it into a tracked good-first-issue checklist.
- Highlight user wins ("incorporated with Keel this weekend") in Discussions and on X.

---

## Week 6 — Consolidate & compound

- Write the **"6 weeks, N stars, what worked"** retro post — this itself is HN-worthy and recruits the next wave.
- Lock in the **recurring content cadence** (one walkthrough + one founder story per week).
- Set up **GitHub Sponsors** / a clear sustainability note so momentum has somewhere to go.
- Define **v1.0** publicly (roadmap issue) so the project reads as durable, not a launch-week stunt.

---

## Channels, ranked by expected leverage

| Channel | Effort | Expected impact | When |
|---|---|---|---|
| Show HN | Med | 🔥🔥🔥 | Wk 1 |
| Product Hunt | Med | 🔥🔥 | Wk 2 |
| Founder X/Twitter thread | Low | 🔥🔥 | Wk 2 |
| Anthropic devrel amplification | Low (outreach) | 🔥🔥🔥 if it lands | Wk 1–4 |
| Reddit (r/startups etc.) | Low | 🔥 | Wk 1–3 |
| awesome-list inclusion | Low | 🔥 (durable) | Wk 4 |
| Comparison/SEO posts | High | 🔥🔥 (compounding) | Wk 3–6 |
| Accelerator partnerships | High | 🔥🔥 (durable) | Wk 4–6 |

## What virality actually requires (the honest part)

Stars follow **trust + an undeniable demo**, not hype. The two things most
likely to sink this:
1. **The demo doesn't work on someone else's machine** → fix install + a hosted try-it before announcing.
2. **It overpromises** ("auto-files your incorporation!") and a founder gets burned → the prepare-to-submit framing is a feature, not a hedge. Say exactly what it does and doesn't do, everywhere. Credibility is the moat.
