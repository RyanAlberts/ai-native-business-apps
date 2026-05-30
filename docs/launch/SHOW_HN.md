# Show HN — draft

**Title (≤80 chars, no emoji, no hype words):**

```
Show HN: Keel – open-source AI back-office for founders (alternative to Atlas)
```

**URL:** the GitHub repo.

---

## First comment (post immediately, from your own account)

I built Keel because the first month of starting a company is a stack of
boring, high-stakes paperwork — incorporate, EIN, the 83(b) election (miss
the 30-day window and it's gone forever), operating agreement, bank account,
sales-tax nexus, a compliance calendar — and the existing options are either
a $500 walled garden (Stripe Atlas, DE-C-Corp-only) or a pile of LangChain
snippets that want an API key per run.

Keel is a fleet of hand-built AI agents with one flagship orchestrator, the
**Founding Journey**: you fill in your company once and it runs incorporation
→ 83(b) → legal docs → banking → compliance in the correct real-world order,
threading a single shared `company.json` through each step, then synthesizes
one Day-0 Formation Packet. It hands you the *actual files* — a printable
packet, the 83(b) letter, an operating agreement, and a real `.ics`
compliance calendar you import — not just a chat transcript.

Two deliberate design calls:

- **It's "prepare-to-submit," not auto-file.** It gets you all the way to the
  submit button on the official .gov portals and pre-fills what it can, but a
  human reviews and submits. I think auto-filing legal/tax docs for strangers
  is irresponsible, and the calendar deadlines are computed deterministically
  from your facts (formation date, state, entity type) rather than parsed out
  of model output, so the dates are trustworthy.
- **It runs on the Claude subscription you already pay for.** It's built on
  the Claude Agent SDK, not a bespoke wrapper — no extra API spend, no
  telemetry, the provider is one line in a config file (OpenAI/Gemini/local
  Ollama also work).

It's Apache-2.0 — fork it, run it for your accelerator's whole batch, add your
own agent by copying a folder.

Honest limitations: the 50-state portal data is hand-curated and some URLs
will go stale (PRs very welcome — there's a tracked "add your state" issue);
non-US is out of scope today; and I'd love a second set of eyes on the
tax/legal prompts. The whole orchestration pipeline is unit-tested offline
with a fake LLM, but the live golden runs are still being captured.

Happy to answer anything about the architecture (the Agent-SDK + MCP tool
routing was the interesting part) or the formation logic.

---

## Prep checklist before posting
- [ ] Hero GIF renders on github.com.
- [ ] `pipx install git+…` verified on a clean machine.
- [ ] CI badge green.
- [ ] 5–10 genuine early stars (friends who actually ran it).
- [ ] You're free for the next 6 hours to reply to every comment.
- [ ] `good-first-issue`s exist for the "how can I help?" replies.
