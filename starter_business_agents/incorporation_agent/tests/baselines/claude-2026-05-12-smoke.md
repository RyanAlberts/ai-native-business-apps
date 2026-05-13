Here is your full incorporation strategy. All URLs come directly from the official Texas SoS and federal portals returned by the tools.

---

## Disclaimer

This is not legal or tax advice. I am an AI strategist, not a licensed attorney or CPA. Filing fees, tax thresholds, and compliance deadlines change frequently — the figures below reflect data retrieved today (May 12, 2026) but should be verified before you file. Please consult a Texas-licensed attorney and/or CPA before making any legal or tax elections, especially around franchise tax filings and any future S-Corp election.

---

## Recommendation Summary

Form a **single-member LLC in Texas**. For a solo, bootstrapped SaaS founder with no employees, no outside investors, and no near-term plans to raise venture capital, a Texas LLC hits the sweet spot: strong personal liability protection, pass-through taxation (no double tax), minimal ongoing compliance cost, and zero state income tax. There is no meaningful reason to form in Delaware or Wyoming given your situation — staying in Texas keeps costs low and avoids the dual-state foreign-qualification headache.

**One flag before anything else:** "Acme" is one of the most overused business name prefixes in the US. Your SoS name search may surface many conflicts, and "Acme Books" could face a rejection on "deceptively similar" grounds. Have a backup name ready.

---

## Entity Type

**Single-Member LLC**

A single-member LLC gives you a legal firewall between your personal assets and business liabilities — critical for a SaaS product where a client (an accountant's firm) could allege data errors, data loss, or professional harm. It is vastly simpler than a corporation: no board, no stock issuance, no annual meeting minutes required. For tax purposes, the IRS treats a single-member LLC as a **disregarded entity** by default, meaning all profit flows to your personal Schedule C — straightforward for a bootstrapped founder. When your net profit grows substantially (often cited around $50–80K+), discuss with your CPA whether electing **S-Corp tax treatment** (via Form 2553) would reduce self-employment tax; that election can be made later without re-forming the entity.

---

## State of Formation

**Texas**

You live and work here, your customers are likely US-based, and Texas has no state income tax — a meaningful advantage over California, New York, or Illinois. The Certificate of Formation fee is **$300** (one-time). The ongoing cost is effectively **$0** for most small businesses: Texas has no annual report requirement, only an annual **franchise tax filing** due May 15 — but entities under the $2.47M revenue threshold owe $0 and simply file a "No Tax Due" report. Compare that to Delaware ($90 franchise fee + $50 registered agent minimum, plus mandatory foreign qualification in Texas anyway at ~$750) — Delaware makes no sense unless you're raising a priced VC round.

---

## Filing Checklist

1. **Verify name availability** for "Acme Books" at the [Texas SoS SOSDirect name search](https://direct.sos.state.tx.us/acct/acct-login.asp). ⚠️ You must create a free SOSDirect account to search. Search the exact name *and* the root word "Acme" alone — expect many hits. Also search for "Books" + "accounting software" combos. If the name is taken or flagged as deceptively similar, have a backup ready.

2. **Run a federal trademark check** at [USPTO TESS](https://tmsearch.uspto.gov/search/search-information) for "Acme Books" in International Classes 35 (business software) and 42 (SaaS/technology services). "Acme" is so generic it may be unregistrable as a standalone mark — important to know before you build a brand around it.

3. **File your Certificate of Formation** (Texas's term for Articles of Organization) with the [Texas Secretary of State](https://www.sos.state.tx.us/corp/forms_boc.shtml). Filing fee: **$300**. You can file online via SOSDirect or mail Form 205. The SoS typically processes in 3–5 business days online.

4. **Designate a Registered Agent** at the time of filing. See the Registered Agent Options section below. The state's registered agent rules are summarized at the [Texas SoS Registered Agent page](https://www.sos.state.tx.us/corp/registeredagent.shtml).

5. **Apply for an EIN (Employer Identification Number)** at the [IRS EIN Online Portal](https://www.irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online). Free, ~15 minutes, instant issuance. Do this immediately after your Certificate of Formation is approved. You need the EIN to open a business bank account.

6. **Open a dedicated business bank account.** Use your EIN + Certificate of Formation approval notice. This is non-negotiable for maintaining the liability shield — commingled finances are the #1 reason courts pierce the LLC veil.

7. **File your BOI (Beneficial Ownership Information) report** with [FinCEN](https://boiefiling.fincen.gov/) within **90 days of formation** (post–Corporate Transparency Act). Free to file. You'll need your personal ID, address, and DOB ready. See [FinCEN BOI FAQs](https://www.fincen.gov/boi-faqs) for what counts as a "beneficial owner."

8. **Draft a Single-Member Operating Agreement.** Texas does not legally require one, but every bank and many enterprise clients will ask for it. It also reinforces that the LLC is a separate legal entity. See the Key Documents section below.

9. **Register for Texas franchise tax** via the [Texas Comptroller](https://comptroller.texas.gov/taxes/franchise/). Even if you owe $0, you must file the "No Tax Due" report annually by May 15. Set a calendar reminder now.

10. **Check city/county business license requirements.** Texas has no state-level business license, but your city or county may require a general business license or a home occupation permit if you're working from a residence. Check your city's website directly (e.g., City of Austin, City of Dallas, etc.).

---

## Key Documents & Artifacts

| Document | Required? | What It Is | Key Trade-offs / Decisions | Follow-up Question to Ask AI |
|---|---|---|---|---|
| **Certificate of Formation** | ✅ Yes — state filing | The legal document that creates your LLC with the Texas SoS | Registered agent name/address is public record; choose carefully. Purpose clause: keep it broad ("any lawful purpose") | "What should I include in my Certificate of Formation for a Texas single-member LLC?" |
| **Operating Agreement** | ⚠️ Not legally required in TX, but strongly recommended | Internal document defining LLC ownership, management rules, and profit/loss allocation | Single-member version is simpler than multi-member; key clauses: capital contributions, dissolution, IP assignment to the LLC | "Draft a single-member LLC Operating Agreement for a Texas SaaS company — include an IP assignment clause." |
| **EIN Confirmation Letter (IRS CP 575)** | ✅ Yes | IRS letter confirming your EIN; needed to open bank accounts and sign contracts | Save the PDF — banks will ask for it. If lost, request an EIN verification letter (147C) by phone | "What do I do if I lose my IRS CP 575 EIN confirmation letter?" |
| **BOI Report (FinCEN)** | ✅ Yes — federal (post-CTA) | Discloses beneficial owners to FinCEN; required within 90 days of formation | Failure to file: civil penalties up to $591/day. Solo founder = you are the sole beneficial owner | "Walk me through filing my BOI report — what info do I need ready for a single-member LLC?" |
| **Registered Agent Designation** | ✅ Yes — included in Certificate of Formation | Names the person/service authorized to receive legal documents | Using your home address makes it public record. See RA Options section | "What are the consequences of missing a service of process as my own registered agent in Texas?" |
| **Annual Franchise Tax Filing** | ✅ Yes — state, every May 15 | "No Tax Due" report filed with Texas Comptroller if revenue < $2.47M | Must file even if $0 owed; failure triggers penalties and potential LLC forfeiture | "What does the Texas franchise tax 'No Tax Due' report look like for a single-member LLC with under $100K revenue?" |
| **Business Bank Account Resolution** | ⚠️ Recommended | Brief document authorizing you (as sole member) to open and operate the bank account | Banks often have their own form; your Operating Agreement usually satisfies this | "Draft a single-member LLC banking resolution I can bring to a bank to open a business checking account." |
| **S-Corp Election — Form 2553** | ❌ Not now — revisit at ~$50–80K net profit | IRS election to tax the LLC as an S-Corp, potentially reducing self-employment tax | Timing matters: election can be made retroactively in some cases; CPA guidance is essential | "What's the difference in self-employment tax savings between staying a disregarded entity vs. electing S-Corp status at $75K annual profit in Texas?" |
| **Software Subscription Agreement / Terms of Service** | ⚠️ Strongly recommended for SaaS | Customer-facing contract limiting your liability for accounting errors | Limitation-of-liability clause is critical when selling to accountants who rely on your data | "What clauses should a SaaS Terms of Service include to limit liability when selling to licensed accountants?" |

---

## Registered Agent Options

### 1. Act as Your Own Registered Agent — $0/year

You can serve as your own RA in Texas using your home address. **However:** your home address becomes part of the permanent public record on the Texas SoS website — indexed by Google, scraped by data brokers, and a magnet for junk mail and solicitors. You must also be physically present at that address during normal business hours to accept service of process (a lawsuit can't wait for you to come back from vacation). If you move, you must file a change with the SoS. **Best for:** founders with a separate commercial office address and zero privacy concerns. Not recommended for home-based founders.

### 2. Traditional Registered Agent Services — ~$100–$250/year

- **Northwest Registered Agent** — ~$125/year. The top pick for privacy-conscious founders. They use their own address everywhere, scan and digitize your mail fast, have US-based phone support, and explicitly do not sell your data. No upsell pressure. Most founder communities recommend them first.
- **Registered Agents Inc.** — ~$200/year. Strong multi-state support, good for founders planning to expand operations to other states.
- **Harbor Compliance** — ~$99–$200/year. Geared toward compliance-heavy industries; useful if you eventually need state licensing in regulated sectors.
- **LegalZoom** — ~$249/year. Recognizable brand but notorious for upselling compliance packages and add-ons you don't need. Customer service reviews are mixed. Only choose if you're already deep in a LegalZoom bundle.

### 3. Digital / Online-First RA Services — $0–$300/year (often bundled)

- **Bizee (formerly IncFile)** — Free RA for year 1, ~$119/year after. Cheap entry point; service quality is improving but still mixed.
- **ZenBusiness** — ~$199/year. Modern dashboard, decent UX, some upsell pressure. Good middle ground.
- **Doola** — ~$300/year bundled with formation. Strong for non-US founders or fully digital businesses.
- **Stripe Atlas** — RA included in their $500 package, but **Delaware C-Corp only** — not applicable here.

### Comparison Table

| Category | Cost/year | Privacy | Mail Handling | Customer Service | Multi-state? |
|---|---|---|---|---|---|
| Self (own RA) | $0 | ❌ Home address public | Manual — you collect it | N/A | No — re-file in each state |
| Northwest / RAI / Harbor | $100–$250 | ✅ Strong | Mail scan, fast turnaround | Generally strong | Yes |
| LegalZoom | ~$249 | Standard | Mail scan | Mixed | Yes (with upsells) |
| Bizee / ZenBusiness / Doola | $0–$300 | Standard | App-based scan | Mixed | Varies |

### 🏆 Top Pick for You

**Northwest Registered Agent (~$125/year).** You're working from home, selling to accountants (who may eventually send legal notices), and privacy matters. Northwest keeps your home address off the public record, scans documents quickly, and won't spam you with upsells. Worth every dollar of the $125.

---

## Estimated Costs

| Line Item | Estimated Cost |
|---|---|
| Texas Certificate of Formation (one-time) | **$300** |
| Registered Agent — Northwest (year 1) | **~$125** |
| EIN application (IRS) | **$0 — free** |
| BOI report (FinCEN) | **$0 — free** |
| Operating Agreement (DIY template) | **$0–$50** |
| Operating Agreement (attorney-drafted) | **$300–$1,500** |
| Business license (city-dependent) | **$0–$75** |
| Texas franchise tax filing (annual, No Tax Due) | **$0** (below $2.47M threshold) |
| **Total to form** | **~$425–$2,000** |
| **Annual ongoing cost** | **~$125–$200/year** |

---

## Common Pitfalls for Your Situation

- **⚠️ Name conflict is a real risk.** "Acme" is one of the most saturated prefixes in US business registries. Prepare a backup name before filing — if the SoS rejects "Acme Books" on deceptively-similar grounds, you'll lose time and potentially re-pay the $300 fee. Also check USPTO TESS: a federally registered "Acme Books" trademark in your software/accounting class could force a rebrand later.

- **⚠️ Missing the BOI 90-day deadline.** FinCEN penalties are civil ($591/day) and the clock starts the day your Certificate of Formation is approved — not when you open a bank account or go live. File the BOI report the same week you receive your Certificate.

- **⚠️ Commingling personal and business finances.** This is the #1 reason courts disregard the LLC and hold founders personally liable. Open a dedicated business checking account immediately after you have your EIN. Every SaaS subscription, hosting bill, and tool renewal goes through that account — nothing personal.

- **⚠️ Missing the May 15 franchise tax filing.** Even at zero revenue you owe the filing. Texas will administratively forfeit your LLC (stripping your liability protection) after missed filings. Set a recurring May 1 calendar reminder as your "file franchise tax" prompt.

- **⚠️ Selling to accountants without a solid Terms of Service.** Accountants rely on software for client data and compliance. A bug that corrupts a client's books or causes a missed filing could generate a professional-liability claim against you. Get a SaaS-specific limitation-of-liability clause in place before you take on your first paying customer — even informally.
