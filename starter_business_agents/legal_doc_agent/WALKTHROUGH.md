# Walkthrough — Legal Document Generator

> "I need an NDA before I can take a sales call. I also need an operating
> agreement, a cofounder split memo, and a Terms of Service. I have 30 minutes."

This agent generates the FIRST DRAFT of those documents. Not the final
version — an attorney sees that — but a complete, internally-consistent
draft the attorney can edit instead of writing from a blank page.

## What you'll see

Pick "Mutual NDA" from the dropdown, fill in the business + parties + term,
hit "Draft document." You get markdown with:

1. **Document type & scope** — restates what's being drafted and the context.
2. **Key choices made** — every default the agent picked. Critical: read
   this first, because it'll say things like *"Defaulted to Delaware
   governing law since your LLC is Delaware-formed; change if you sue
   most often in CA."*
3. **The document itself** — actual draft text, defined terms in bold,
   signature blocks with `[BRACKETED PLACEHOLDERS]` for search-and-replace.
4. **Clauses to negotiate or red-flag** — the parts attorneys focus on.
5. **State-specific considerations** — what changes by state.
6. **Common founder mistakes for this doc type** — e.g. signing a mutual
   NDA when only outbound disclosure was needed.
7. **Next steps** ending in *"have a licensed attorney review."*

## How it works

One LLM call, temperature 0.1 (deterministic — legal docs shouldn't be
creative), `max_tokens: 8192` so full operating agreements have room. The
prompt enforces the section structure and the "Key choices made" disclosure
that makes the output safer to use.

## Customizing it

### Add a new document type

1. Edit `app.py::DOC_TYPES` — append your new type.
2. (Optional) Edit `prompts.py::SYSTEM_PROMPT` to mention any unusual
   structure for that type — the LLM handles most cases without prompt
   changes.

### Make it state-specific by default

In `prompts.py`, add to the "State-specific considerations" section a rule
like *"If state is California, include a section on California
Bus. & Prof. Code §16600 around non-competes."* The agent will follow it.

### Swap to OpenAI for higher consistency

```yaml
# config.yaml
provider: openai
model: gpt-4o
temperature: 0.0
```

For legal-doc drafting, gpt-4o at temperature 0 is also good. Cost: a few
cents per draft on API.

## Going further

- Pair with the [**Incorporation Agent**](../incorporation_agent/) — the
  operating agreement comes right after formation.
- Pair with the [**Loan Agent**](../loan_application_agent/) — SBA loans
  often require operating agreements, personal financial statements,
  guarantor agreements.
- The [**Cofounder Agreement**](#supported-document-types) option is the
  single highest-leverage doc a founder team can run early. Use this agent
  to draft it the week you decide to work together.

## Footer

From **AI-Native Business Apps** — hand-built, provider-agnostic, Apache-2.0.
Templates only — get attorney review.
