# Parity Report — Business License + DBA Agent

| | |
|---|---|
| Source | Original work; DBA jurisdiction + general-state-license data hand-curated from each state's authoritative site |
| Default model | claude-sonnet-4-6 |
| Last verified | not yet run end-to-end |

## 1. Capability parity (tools × providers)

| Tool / Capability | claude | openai | gemini | xai | ollama | codex |
|---|---|---|---|---|---|---|
| `dba_filing_jurisdiction` | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ stub |
| `state_general_business_license` | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ stub |
| WebSearch (provider built-in) | ✅ | ⚠️ MCP/custom | ⚠️ MCP/custom | ⚠️ MCP/custom | ❌ | ⏳ stub |

Without WebSearch, the agent can still produce state-level DBA + general-
license guidance but cannot identify the founder's specific city/county
licenses or industry-specific state permits — degraded mode.

## 2. Behavioral parity (golden prompts)

See `tests/golden.jsonl`.

| ID | Scenario | claude | openai | gemini |
|---|---|---|---|---|
| g1 | SF coffee shop (food + beer/wine + sidewalk seating; max-fragmented) | not yet run | not yet run | not yet run |
| g2 | Home-based WY-LLC SaaS, founder in TX (mismatch state of formation vs operation) | not yet run | not yet run | not yet run |
| g3 | MA cleaning service (city-level DBA; multiple low-friction layers) | not yet run | not yet run | not yet run |
| g4 | NV retailer (one of the 5 general-state-license states) | not yet run | not yet run | not yet run |
| g5 | DE contractor (contractor licensing layer + general DE license) | not yet run | not yet run | not yet run |

## 3. UX parity (Streamlit)

- [x] Form-based input (not free text) with structured selectors:
      entity, DBA, industry, city, state, county, employees, premises,
      home-based, sells goods, industry triggers
- [x] Industry-triggers multi-select to pre-load the right permit
      categories for the LLM
- [x] Download button

## 4. Cost / latency

One or more WebSearch tool calls + a few deterministic tool calls.
Expected wall time: 30–60s. Less than the multi-stage agents.

## 5. Known gaps

- **Long-tail jurisdictions not curated**: city and county data come
  from WebSearch, not from a hand-curated table. Snapshot drift between
  WebSearch runs is possible.
- **Industry-specific federal licensing**: the prompt lists common
  triggers (ATF, FAA, FCC, SEC, FDA, DOT, MSHA) but the agent doesn't
  have a tool for them; relies on the LLM's training + WebSearch.
- **No quote-engine**: ABC liquor licenses, food permits, etc. all have
  application fees published online, but actual processing costs vary.
  Agent gives ranges; doesn't book appointments or estimate exact total.
- **DBA renewal cadence**: states differ wildly (5 years, 10 years,
  never). The tool's `notes` field captures some of this; not all.
- **Zoning verification**: the agent flags zoning as a separate
  concern but cannot verify a specific address's zoning code without
  city-level GIS data.

## 6. Verdict

| Provider | Verdict |
|---|---|
| claude | not yet verified (scaffold + tools shipped; needs end-to-end run with WebSearch) |
| openai | not yet run; requires MCP search or custom Tool for WebSearch |
| gemini | not yet run; requires MCP search or custom Tool for WebSearch |
| xai | community-supported |
| ollama | not supported (no native web search) |
| codex | stub |
