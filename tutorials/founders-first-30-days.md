# Founder's First 30 Days — A Complete Walkthrough

> Tutorial that uses **8 agents** in sequence to get from "I have a business
> idea" to "I'm legally formed, banked, insured, compliant, and have a
> website live." Real chronology, real choices, real artifacts.

---

## Who this is for

You just decided to start a business. You're solo or 2 people, bootstrapping
or planning a small seed round, and you want to use AI to compress 100 hours
of tedious setup work into about 20 hours of decision-making + paperwork.

You don't need to be technical. You need:
1. A computer with Python 3.11+ installed
2. A Claude Max subscription (or an OpenAI / Gemini API key)
3. About 30 days of evenings

By the end you'll have an LLC (or whatever entity fits), an EIN, a bank
account, the right insurance, a compliance calendar, a website, and the
first draft of every legal document you'll need.

---

## Set up once (10 minutes)

```bash
pipx install git+https://github.com/RyanAlberts/ai-native-business-apps.git
```

That's it. The `agent` command is now on your PATH. Run `agent list` to see
every agent in the repo.

If you have Claude Max, log into the `claude` CLI once (`claude login`) and
no API keys are needed. If you don't, set `OPENAI_API_KEY` (or
`GOOGLE_API_KEY`) in your `.env` and update each agent's `config.yaml` with
`provider: openai` (or `gemini`).

---

## A worked example: Sarah's compliance SaaS

I'll narrate this walkthrough through **Sarah** — a former compliance
consultant who's about to leave her job to build a SaaS that automates
SOC 2 evidence collection for small fintechs. She's solo, based in
Austin, Texas, and has $50k savings to fund 6 months of focused work.
She's not raising VC in year 1.

If your situation is different, the agents adapt — Sarah's story is just
to ground the steps.

---

## Days 1–3 · Test the strategy before committing

Even good ideas fail when the founder hasn't pressure-tested them.
Before incorporating, run the **Business Plan Implementation Manager**.

```bash
agent business-plan
```

Sarah pastes:

> *"AI-native SaaS that automates SOC 2 evidence collection for small
> fintechs (Series A-B, 20–100 employees). I was a compliance consultant
> for 6 years. $50k savings, 6 months runway, no VC plans in year 1."*

Over ~2 minutes the agent runs 4 stages: **Market Research → SWOT →
Strategy → 30/60/90 Roadmap**. She gets:

- A market brief naming the real players (Vanta, Drata, Secureframe,
  Tugboat Logic) and how they're priced
- A SWOT specifically pitting her domain expertise against Vanta's
  distribution advantage
- A strategic recommendation: don't compete head-on; focus on the segment
  Vanta deprioritized (fintechs under 50 people who can't justify $25k+
  annual contracts)
- A 30/60/90 roadmap starting with "land 3 pilot customers at $300/mo via
  cold outreach to fintech CTOs"

Sarah saves the markdown output. **Key call this stage forces her to
make**: beachhead segment + pricing wedge. She locks "sub-50-person
fintechs, $300/mo, cold-outreach GTM."

→ See: [Business Plan Implementation Manager walkthrough](../advanced_business_agents/multi_agent_apps/business_plan_implementation_manager/WALKTHROUGH.md)

---

## Days 4–7 · Incorporate, get an EIN

With strategy locked, it's time to legally exist. Run the **Incorporation
Agent**.

```bash
agent incorporation
```

Sarah enters:
- Business: "SOC Squared" (proposed)
- State: Texas
- Cofounders: 1 (just her)
- Funding plans: bootstrap → friends & family
- Hiring plans: just founders

The agent recommends a **single-member LLC in Texas**, not Delaware. It
explains the reasoning (no near-term VC, no operational benefit to a
foreign filing, Texas franchise tax is simpler than DE annual report +
foreign LLC fee in TX).

She gets:
- Filing checklist with direct URLs to the Texas SOS portal
- Registered-agent options including LegalZoom, Northwest Registered
  Agent, and the cost/privacy/junk-mail trade-offs of acting as her own
- Pitfalls specific to a solo founder (commingling funds, missing the
  BOI deadline, no operating agreement)
- A Key Documents table she can use as her checklist

**This week's tasks**:
1. File Texas Certificate of Formation (Form 205) — $300, sosupload.sos.state.tx.us
2. Apply for EIN at irs.gov/EIN — free, ~15 minutes
3. File BOI report at boiefiling.fincen.gov within 90 days
4. Pick a registered agent

→ See: [Incorporation Agent walkthrough](../starter_business_agents/incorporation_agent/WALKTHROUGH.md)

---

## Days 8–12 · Operating agreement + contractor templates

Even as a single-member LLC, an Operating Agreement is the doc that keeps
the corporate veil intact in court. Sarah also wants templates ready for
the engineer she'll contract.

```bash
agent legal-doc
```

She runs it twice:

**Run 1**: Single-member LLC Operating Agreement, Texas-formed,
manager-managed, member is herself.
She gets a full draft (~3,000 words) with defined terms, distribution
rules, transfer restrictions, dissolution mechanics, indemnification.
The "Key choices made" section flags what the agent defaulted to (e.g.
*"Defaulted to manager-managed since you're solo; member-managed makes
multi-member adds cleaner — change if you plan to add a cofounder
within 12 months."*). She sends it to her business attorney for a $400
review pass.

**Run 2**: Independent Contractor Agreement for a CA-based engineer,
$120/hr, project basis, work-for-hire IP assignment.
She gets a ready-to-fill template covering scope, deliverables,
payment terms, IP assignment, confidentiality, indemnification. She
keeps it as a template; will paste actual contractor names per gig.

Other docs Sarah will run through this agent as the year unfolds: NDA
(before pitching to design partners), Privacy Policy + ToS (before
launching the website), Service Agreement / SOW (for her first paid
pilots).

**Important**: every output ends with a disclaimer to get attorney
review. Sarah does that — she sends both drafts to a small-business
attorney via UpCounsel for a flat $400 review on both docs.

→ See: [Legal Document Generator walkthrough](../starter_business_agents/legal_doc_agent/WALKTHROUGH.md)

---

## Days 13–17 · Bank + insurance

Now that she has Articles, EIN, and operating agreement in hand, she
can open a bank account. And once there's money in it, she needs
liability cover.

```bash
agent bank-insurance
```

She enters:
- Business: SOC Squared LLC (SaaS for compliance, Texas)
- Stage: pre-revenue
- Employees: just founder
- Physical space: fully remote
- Customer data: customer-data summaries (not PHI / not card data — Stripe handles cards)

The agent recommends:
- **Banking**: Mercury (digital-native, no monthly fees, integrates with
  every accounting tool, FDIC sweep across 5 partner banks for $5M
  coverage). Backup: local credit union for a "real banker" relationship
  when she eventually wants a line of credit.
- **Insurance**: 
  - **Professional Liability (E&O)** — $1M/$2M aggregate, ~$1,200/yr
    (Hiscox or Next Insurance). She gives advice + software; this is her
    biggest exposure.
  - **Cyber Liability** — $1M, ~$1,500/yr. She stores customer compliance
    data summaries.
  - **General Liability** — $1M/$2M, ~$500/yr. Standard SMB cover.
  - **NOT yet**: workers' comp (no employees), D&O (no investors), EPLI
    (no employees), Commercial Auto (no vehicles).

Sarah gets quotes from Hiscox + Next in week 1, binds both within 5
days. Total first-year insurance: ~$3,200.

→ See: [Bank & Insurance walkthrough](../starter_business_agents/bank_insurance_agent/WALKTHROUGH.md)

---

## Days 18–22 · Compliance + tax setup

Now that money is moving, Sarah needs to know what she owes whom, when,
and how to track it.

```bash
agent compliance-tax
```

She enters:
- Single-member LLC, Texas-formed and -operated
- Pre-revenue but expects $30k in year 1, $200k+ in year 2
- Sales channels: direct to fintechs via her own website
- No employees; she'll pay 1 contractor mostly remote

The agent maps:

**Sales tax nexus**: She has physical nexus in TX (lives + works
there). Most US states don't tax SaaS, but a handful do (e.g. WA, NY,
CT, TX itself). For TX, SaaS IS taxable — but only on the "20% of
charges" portion attributed to data-processing under TX rule 3.330.
She needs to register with the TX Comptroller for sales tax once she
starts billing TX customers.

**Federal filings**: Form 1040 with Schedule C (single-member LLC
default treatment), quarterly estimated taxes (1040-ES), 1099-NEC for
the contractor at year-end, BOI within 90 days of formation.

**State filings**: Texas Franchise Tax due May 15 each year (zero owed
under the no-tax-due threshold of $1.23M revenue, but the form is still
required). Public Information Report due same date.

**Bookkeeping**: Recommends QuickBooks Online ($30/mo, accountant
compatible). Wave is free but she'll outgrow it once she has multiple
revenue streams.

**Advisor cadence**: Hire a CPA before year-end Q4 to prep year 1
taxes; not earlier. Hire a monthly bookkeeper when revenue passes
$10k/mo.

She bookmarks the IRS, TX Comptroller, and FinCEN URLs from the
agent's output as her ongoing reference.

→ See: [Compliance & Tax walkthrough](../starter_business_agents/compliance_tax_agent/WALKTHROUGH.md)

---

## Days 23–27 · Funding (optional — only if you need it)

Sarah is bootstrapping, so she runs this only to evaluate emergency
backup options. If your runway is tighter, this is where you'd start
applying.

```bash
agent loan
```

She enters:
- Pre-revenue solo SaaS, Austin TX
- $40k contemplated need (only if MVP timeline slips)
- Founder credit 740, no business credit history, $50k personal savings,
  owns home with $80k equity

The agent ranks:
1. **SBA Microloan via LiftFund (Austin)** — strong fit. Pre-revenue
   acceptable, no collateral required at this amount, 30-60 days from
   complete application.
2. **LiftFund direct CDFI loan** — backup, faster (2-6 weeks), slightly
   higher rates.
3. **Bootstrap from the home-equity HELOC** — readily available, low
   rate, but mixes personal + business risk.

Sarah doesn't actually apply; she notes LiftFund as her emergency
fallback if month-4 looks tight, and sets a calendar reminder to
re-evaluate at the 60-day mark.

→ See: [Loan & Funding walkthrough](../starter_business_agents/loan_application_agent/WALKTHROUGH.md)

---

## Days 28–30 · Website live

By day 28, Sarah has corporate formation, banking, insurance, compliance,
and a strategic plan. Now the public face.

```bash
agent website-launch
```

She enters:
- Business: AI-native SaaS for SOC 2 automation, sub-50-person fintechs
- Target: CTOs at Series A-B fintechs (20-100 people)
- Background: 6 years compliance consulting
- Budget: $5k for site + launch; live in 7 days

Over 4 stages she gets:

**Brand & Domain**: Recommended name "SOCwise" (alternates: Squared,
Compyne, Loop) + `.com` strategy + brand voice ("technical but
warm-expert; we know your auditors hate audits as much as you do") +
color palette + Inter / Source Sans fonts.

**Site Architecture**: 5-page marketing site recommended (Home, Pricing,
Customers, Blog, About). Conversion path: Home → Pricing → Free SOC 2
readiness check → Email capture → 7-day nurture sequence → Pilot
conversation booked. Tech stack: Framer for v1 (she's not technical
enough to maintain Next.js; can migrate later).

**Copy & Design**: Hero — *"SOC 2 evidence collection that fintechs
actually finish. Without the consulting bill."* Subheadline + 3 feature
blocks + social-proof placeholders (she'll fill with pilot customers in
month 2) + pricing copy.

**Launch Checklist**: Day -7 to day +30 with concrete tasks including
DNS setup, hosting, GA4 install, accessibility QA on 3 viewports, legal
pages (Privacy Policy + ToS — she runs `agent legal-doc` for these
again), favicon, social preview cards, sitemap submission to Google +
Bing, day-0 announcement to her LinkedIn + 3 fintech communities.

She works through it across days 28-30 with Framer. Site is live on
day 30 at socwise.com (an actual `.com` she registered for $15 at
Cloudflare).

→ See: [Website Launch Team walkthrough](../advanced_business_agents/multi_agent_apps/website_launch_team/WALKTHROUGH.md)

---

## What Sarah has on day 30

| | Artifact |
|---|---|
| ✅ | Texas LLC formed, EIN issued, BOI filed |
| ✅ | Operating Agreement (attorney-reviewed) |
| ✅ | Independent Contractor Agreement template |
| ✅ | Mercury business bank account |
| ✅ | E&O + Cyber + GL insurance bound |
| ✅ | Compliance calendar + QuickBooks set up |
| ✅ | Funding emergency-fallback identified |
| ✅ | Live marketing site with Privacy Policy + ToS |
| ✅ | Strategic plan with 30/60/90 milestones |

Total cost: ~$3,800 first-year operating cost (filings + insurance +
bookkeeping software) + a $400 attorney review. About 25 hours of her
time across 30 days.

For comparison: doing this the "old way" — hiring a small-business
attorney for incorporation paperwork ($1,500), a bookkeeper for setup
($800), an insurance broker, a designer for the website ($5–15k), a
business consultant for the strategy work ($3-10k) — would cost
$10–25k and take 60–90 days.

The agents don't replace the attorney review or the CPA at year-end.
They get the founder 80% of the way there, so the professional time
they pay for is high-leverage review work, not blank-page drafting.

---

## When to use each agent (cheat sheet)

| When | Agent | Time |
|---|---|---|
| Got an idea, haven't committed | `business-plan` | 2 min |
| About to file with the SoS | `incorporation` | 30 sec |
| Need a doc you'd otherwise pay $500 for | `legal-doc` | 1 min per doc |
| Just got your EIN | `bank-insurance` | 30 sec |
| Need to know what you owe whom | `compliance-tax` | 30 sec |
| Need money you don't have yet | `loan` | 30 sec |
| About to build a website | `website-launch` | 2 min |
| Building a physical product | `supplier-sourcing` | 2 min |

---

## What this walkthrough doesn't cover

Year 1, post-day-30 work that's NOT in this repo (yet):

- Hiring (job descriptions, offer letters, equity grants) — likely a
  future `hiring_agent`
- Customer research / interview synthesis — there are good agents
  elsewhere; consider [productivity:synthesize-research](https://github.com/Shubhamsaboo/awesome-llm-apps) for now
- Marketing / cold outreach automation — future work
- Fundraising-track pitch deck and investor outreach — future work
- International incorporation / global expansion — out of scope for v1

If you build an agent that fills a gap, PRs welcome. See
[CONTRIBUTING.md](../CONTRIBUTING.md).

---

## Get in the habit

The most valuable thing about these agents isn't that they generate
output. It's that they force you to commit to specific decisions —
entity type, beachhead segment, insurance coverage levels, pricing —
in writing, in 30 minutes, instead of stalling on them for weeks.

You'll get the output wrong sometimes. The right move is to **re-run
the agent with corrected context** (e.g. *"actually I'm raising a
seed in 6 months, not bootstrapping"*) and let it redo its
recommendation. The agents are cheap; founder time is not.

---

*From [AI-Native Business Apps](https://github.com/RyanAlberts/ai-native-business-apps)
— hand-built, provider-agnostic, Apache-2.0. The toolkit for founders
who want AI baked in from day 0.*
