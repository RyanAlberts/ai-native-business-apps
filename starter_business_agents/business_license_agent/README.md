# Business License + DBA Agent

**What "business license services" charge**: $99–$300 per location for a
checklist of city/county/state/federal licenses. Companies like Bizee,
ZenBusiness, Harbor Compliance, Avalara, and CSC all offer this.

**What LegalZoom and PEOs (Gusto/Rippling) charge**: nothing — they
don't handle city/county licenses at all. LegalZoom files state-level
DBA / fictitious name registration as an add-on (~$99 + state fee).

**What this agent charges**: $0. Open source.

## What it does

For a specific founder situation (entity, industry, city, state, county,
home-based or premises-based, employee count, industry triggers),
produces a structured checklist of:

- **DBA / Fictitious Business Name** registration at the correct level
  (state SoS / county clerk / city clerk / both) — driven by the
  deterministic `dba_filing_jurisdiction` tool covering all 51 US
  jurisdictions
- **State general business license** (only AK / DE / HI / NV / WA have
  one) — driven by the deterministic `state_general_business_license`
  tool
- **State industry-specific licenses** (food, contractor, alcohol,
  cosmetology, professional services, etc.) — via WebSearch
- **County license** / business tax receipt — via WebSearch
- **City business license** + zoning / home-occupation permit — via
  WebSearch
- **Special permits** that apply: home occupation, sign, health, fire,
  resale certificate, entertainment, outdoor seating, etc.
- **Federal layer** when industry triggers it (ATF / FAA / FCC / SEC /
  FDA / DOT)
- **Total approximate year-1 cost** with sources
- **Filing sequence** in the right order
- **Common mistakes** specific to the founder's situation

## Architecture: hybrid deterministic + WebSearch

The agent is a hybrid:

- **Deterministic** for the parts that don't change much: the state-by-
  state DBA-filing-jurisdiction taxonomy (51 states/DC) and the
  state-general-license requirement (5 states have one).
- **WebSearch-driven** for the long-tail: ~3,000 US counties × ~19,000
  US municipalities × thousands of industries. Hand-curating that table
  is out of scope; the LLM + web search points the founder at the
  right city/county portal at runtime.

## Quick start

```bash
# CLI
python -m starter_business_agents.business_license_agent.agent \
  "California LLC operating a coffee shop in San Francisco. Entity 'Mission \
   Coffee LLC' DBA 'The Daily Grind'. 2 employees. Beer/wine planned."

# Streamlit UI
streamlit run starter_business_agents/business_license_agent/app.py
```

## Curated data (51 jurisdictions)

- DBA filing level per state in `tools.py::_DBA_JURISDICTION`
- State general license in `tools.py::_STATE_GENERAL_LICENSE`

When the data is wrong (URL drift, statute change), fix it inline in
the dict and ALL downstream founders benefit immediately. Pull requests
welcome.

## NOT legal advice

Licensing requirements change. Cities and counties revise ordinances
regularly. The URLs returned are snapshots — confirm on the issuing
agency's current site before paying. Consult a business attorney or your
local Small Business Development Center (SBDC, https://americassbdc.org/)
for licensing complexity unique to your industry or city.

## Sources

- DBA / Fictitious Business Name data: each state's SoS site + Cornell
  LII state-by-state survey of fictitious business name statutes
- State general license data: each state's official licensing portal
  (linked inline in the tool output)
- SBA / Small Business Development Center: https://americassbdc.org/
- USA.gov "Find a license" portal: https://www.usa.gov/business
