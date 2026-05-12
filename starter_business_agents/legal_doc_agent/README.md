# 📜 Legal Document Generator

> Draft templates for the boring-but-essential legal docs every founder
> eventually needs: operating agreements, NDAs, IP assignments, contractor
> agreements, ToS, privacy policies, SOWs, cofounder agreements.

## What it does

Takes a document type + business context + parties and returns:

- A complete document draft (usable as a starting point, not a stub)
- "Key choices made" — surfaces every default it picked so you can override
- Clauses to negotiate / red-flag
- State-specific considerations
- Common founder mistakes for this doc type
- A next-steps checklist ending in **get attorney review**

## Supported document types

Operating agreements (single + multi-member), NDAs (mutual + unilateral),
IP assignment, independent contractor, ToS, privacy policy, SOW, cofounder
agreement.

## Run

```bash
agent legal-doc                          # Streamlit UI with dropdown
agent legal-doc --cli "Mutual NDA, software founder LLC <> AcmeCorp Inc., 2-year term, Delaware governing law."
```

## Critical caveat

These are **templates for attorney review**. State law varies; some
industries trigger special rules (HIPAA, COPPA, CCPA, GDPR, FINRA, etc.).
Never sign or publish without a licensed attorney's review.

## Customize

- Edit `prompts.py::SYSTEM_PROMPT` to add a new document type or change
  the section structure.
- Edit `app.py::DOC_TYPES` to expose the new type in the dropdown.

## Provider parity

Verified on Claude (subscription). See [PARITY.md](./PARITY.md).
