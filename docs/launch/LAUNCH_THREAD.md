# X / Twitter launch thread — draft

Lead with the demo GIF in tweet 1. Keep each tweet self-contained.

---

**1/ 🧵** (attach the 60–90s Founding Journey GIF)

I rebuilt Stripe Atlas as an open-source AI agent.

Fill in your company once → get a complete Day-0 formation packet:
incorporation, 83(b), legal docs, banking, a compliance calendar — and the
actual files, ready to file.

$0. Runs on the Claude sub you already pay for. Apache-2.0.

👇

**2/** The first month of a startup is a paperwork minefield:

• incorporate + EIN
• 83(b) election (miss the 30-day window and it's gone *forever*)
• operating agreement
• bank account
• sales-tax nexus
• a compliance calendar

Atlas does a slice of this for $500, DE-C-Corp-only, in a box you don't own.

**3/** Keel's flagship is the **Founding Journey** — one profile, five
specialists threaded in the right real-world order (you can't get an EIN
before the entity exists; you can't open a bank account before the EIN), then
one synthesized packet.

(attach the vs-Atlas comparison table image)

**4/** The part I'm proud of: it hands you **real files**, not a chat log.

📄 a printable Day-0 packet (Save as PDF)
✉️ your 83(b) letter
📜 an operating agreement
📅 a `.ics` calendar of your deadlines you import to Google/Apple

Deadlines are computed deterministically — not parsed out of an LLM.

**5/** It's deliberately **prepare-to-submit**, not auto-file. It takes you all
the way to the submit button on the official .gov portals and pre-fills what
it can — you review and submit. Auto-filing legal/tax docs for strangers is a
liability, not a feature.

**6/** Built on the @AnthropicAI Claude Agent SDK — so for Max users the agent
calls draw on a separate budget, not your chat limits. No API key. No
LangChain. No telemetry. Swap to OpenAI/Gemini/local Ollama with one config
line.

**7/** It's Apache-2.0. Fork it. Run it for your accelerator's whole batch. Add
your own agent by copying a folder.

⭐ Star it / try it: github.com/RyanAlberts/ai-native-business-apps

```
pipx install git+https://github.com/RyanAlberts/ai-native-business-apps.git
keel founding-journey
```

**8/** Building in public. Tell me the founder-task agent you wish existed and
I'll probably build it this week. RTs help other founders find it 🙏

---

## Reusable one-liners (for replies / quote-tweets)
- "It's the open-source Stripe Atlas, and it hands you the actual files."
- "Free, runs on your Claude sub, you own all of it."
- "An agent that won't let you miss the 83(b) 30-day window."
