# Walkthrough — Trademark Search Team

This agent is the multi-sub-agent architectural showcase for the repo.
It's the first consumer of `core.ParallelHarness` and demonstrates how
to fan out concurrent research and consolidate findings.

## Why parallel, not sequential

Trademark conflict research has four genuinely independent searches:

- **Federal TESS** queries the USPTO database.
- **State SoS** registries are 50 distinct state-level systems.
- **Common-law** scanning needs the open web (Google, social, Amazon).
- **Class identification** queries the USPTO ID Manual.

None of these depends on another's output. Running them sequentially
takes 4× as long for no gain. `ParallelHarness` fans them out via
`asyncio.gather` and then passes their consolidated findings to a
synthesizer.

## The flow

```python
ParallelHarness(
    llm=claude,
    branches=[
        Stage("Federal TESS",          system=FEDERAL_TESS_PROMPT,   ...),
        Stage("State TM Registries",   system=STATE_TM_PROMPT,       ...),
        Stage("Common-Law Scan",       system=COMMON_LAW_PROMPT,     ...),
        Stage("Class ID",              system=CLASS_ID_PROMPT,       ...),
    ],
    synthesizer=Stage(
        "Trademark Strategy Synthesis",
        system=SYNTHESIZER_PROMPT,
        tools=[uspto_fee_estimate],
    ),
)
```

Wall-clock latency: roughly `max(branch_durations) + synthesizer_duration`
instead of `sum(branch_durations) + synthesizer_duration`. For a real
trademark search with WebSearch tool calls, the difference is typically
30-60s vs 90-180s — a meaningful UX win.

## What each branch is told

Each branch has a **narrow** system prompt — its only job is to produce
structured findings in a known format. The branches don't draw conclusions;
they produce raw data the synthesizer reasons over.

This is critical because it prevents two failure modes:

1. **Branch overreach**: a single branch trying to render a verdict from
   incomplete data (e.g. "TESS shows nothing, so this mark is clear").
   The synthesizer is the only stage allowed to render verdicts.

2. **Branch divergence**: branches reaching contradictory conclusions
   that have to be reconciled by humans. By design, the synthesizer
   sees raw findings and is the single point of judgment.

## The synthesizer's job

It receives all four branch outputs as a single markdown blob (one
`## Branch: <name>` block per branch). It then:

1. **Maps findings to severity**: a LIVE federal registration for the
   same mark in the same class is HIGH; a DEAD state registration for
   a similar mark in a different class is LOW.

2. **Renders a verdict**: GO / CAUTION / NO-GO. The prompt explicitly
   forbids softening NO-GO results — founders need the honest signal.

3. **Calls `uspto_fee_estimate`**: a deterministic tool that computes
   the filing fee per the post-Jan-2025 USPTO schedule. No LLM math.

4. **Builds the TEAS pre-fill**: the synthesizer outputs the exact
   values the founder will paste into uspto.gov. Fields like applicant
   name, address, signature, and email are left as `[FOUNDER]`
   placeholders — the agent never echoes these back.

5. **Surfaces the calendar**: filing date → examination → office action
   windows → statement of use deadline → year-6 maintenance → year-10
   renewal.

## When the verdict is CAUTION or NO-GO

The synthesizer's next-steps section explicitly recommends an attorney
consultation. The $899 LegalZoom registration becomes a $500-$1,500
boutique attorney review, with the agent's research as the brief.

This is the deliberate positioning: open-source eats the **research +
form-prep** layer of trademark services. We don't displace attorneys
for marginal calls — we let founders walk in with a complete brief
instead of paying for the search hours.

## When the verdict is GO

The synthesizer produces a fillable TEAS Plus application. The founder:

1. Verifies USPTO fees on uspto.gov (URL in the report).
2. Verifies Nice class language on the ID Manual (URL in the report).
3. Re-runs a TESS search themselves right before filing (records change
   weekly; the agent's data is by-definition stale by filing time).
4. Logs into uspto.gov and pastes the pre-fill.
5. Pays the filing fee.
6. Calendars the next windows.

## Failure modes guarded against

| Risk | Guard |
|---|---|
| Hallucinated TESS records | Branch prompts explicitly forbid invention; require source URLs; require "no results" disclosure if WebSearch returns empty. |
| Made-up USPTO fees | Synthesizer must call `uspto_fee_estimate` (deterministic) before writing the fee section. |
| Soft-pedaling NO-GO verdicts | Synthesizer prompt explicitly forbids softening. |
| Echo of personally-identifying info | TEAS pre-fill leaves applicant name/address/email/signature as `[FOUNDER]` placeholders. |
| Stale fee schedule | The fee tool surfaces the USPTO fees page URL and instructs the founder to verify before paying. |

## What it doesn't do

- **File for you.** The TEAS portal requires manual login + payment.
  The agent gives you the pre-fill, not a filed application.
- **Run a TESS search you can rely on without verification.** WebSearch
  is good enough for triage; right-before-filing should be re-run on
  the live TESS interface.
- **Replace an attorney for borderline cases.** When the verdict is
  CAUTION or NO-GO, the report explicitly says "get attorney review".
- **Handle international trademarks (Madrid Protocol, EUIPO, etc.).**
  Adding an EU branch would be a one-line addition; the current scope
  is US-only.

## Extending it

The whole point of `ParallelHarness` is that adding research dimensions
is trivial. Future branches you might add:

- **EU trademarks** (EUIPO eSearch+)
- **Domain availability** (whois + popular TLDs)
- **Social handle availability** (namechk-style)
- **DBA conflicts** in the founder's home county
- **Industry-specific registries** (e.g. UDRP records for domain-name
  conflicts; ICANN for new gTLDs)

Each is a `Stage` with a focused system prompt. The synthesizer prompt
expands to weigh the new findings, but the harness mechanics don't
change.
