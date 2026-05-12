# 📋 Compliance & Tax Setup Agent

> Map sales-tax nexus, state registrations, annual filings, and bookkeeping
> setup for a small business — before tax season catches you off guard.

## What it does

Takes a business profile (entity type, formation state, operation states,
sales channels, employees, revenue) and returns:

- **Sales tax nexus analysis** — physical, economic, marketplace facilitator
- **State registrations needed** — foreign-LLC, sales tax permits, SUI,
  workers' comp, business licenses
- **Federal filings calendar** — income tax, 1099s, W-2s, payroll
- **State filings per state** — annual reports, franchise tax, sales tax
  returns
- **Bookkeeping setup** — one tool pick (QuickBooks, Xero, etc.) + practices
- **Advisor engagement plan** — when to bring in a CPA / bookkeeper / payroll
- **30/60/90-day action plan**

## Run

```bash
agent compliance-tax
agent compliance-tax --cli "Delaware LLC, operating from CA. Shopify+Amazon skincare. $200k yr1. Customers all 50 states."
```

## Why this matters

Most founders learn about sales-tax nexus when they get a notice from a
state DOR saying they owe $30k in back taxes. This agent surfaces nexus
exposure up front — before you've been selling in 47 states for a year.

## Customize

- Add an industry-specific compliance check by editing
  `prompts.py::SYSTEM_PROMPT` — e.g. *"If business serves food, include
  FDA registration and local health-dept permit."*
- Enable WebSearch in `config.yaml::allowed_tools` for current-year nexus
  threshold verification (Claude built-in).

## Provider parity

Verified on Claude. See [PARITY.md](./PARITY.md).
