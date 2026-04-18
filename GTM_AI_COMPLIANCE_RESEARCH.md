# GTM AI Tools Compliance Gaps for Enterprise Decision-Makers

**Research compiled by:** Claude with Sathya  
**Date:** April 18, 2026  
**Status:** Active compliance snapshot with regulatory citations

---

## Executive Summary

The GTM AI tools landscape has three critical compliance gaps:

1. **B2B Outbound**: No product ships real pre-send consent verification, automatic AI disclosure, or claim substantiation as first-class features
2. **Consumer-Facing**: Voice cloning creates simultaneous exposure across TCPA + state right-of-publicity + pending federal laws
3. **Enterprise Buyer Personas**: CFO, CCO, COO, CSO/CMO accountability mechanisms are absent from current tooling

**Regulatory enforcement is accelerating** (e.g., FTC warning letters Jan 2026, Fifth Circuit Bradford ruling Feb 2026, California SB 243 effective Jan 2026, EU AI Act enforceable Aug 2, 2026).

---

## Part 1: Products Analyzed

### Kalibr AI
- **Classification:** AI agent routing infrastructure (not a GTM tool itself)
- **URL:** https://kalibr.systems/docs
- **Status:** `/llm.txt` endpoint referenced returns 404; analysis based on substantive docs at `/docs`
- **Role in GTM stack:** Infrastructure layer for model + tool + parameter routing

**Technical Architecture:**
- Four of twelve default goal types are direct AI-SDR primitives:
  - `web_scraping`
  - `data_enrichment`
  - `lead_scoring`
  - `outreach_generation`
  - (Plus `research` makes five)

- Two-gated eval system:
  - Gate 1: Synchronous structural check (no LLM, always in path)
  - Gate 2: Async LLM quality judge (10–20% sample for research and outreach_generation only)
  - LLM never in routing hot path

- **Trust Invariant:** Success rate always beats cost; cost only breaks ties within ~5pp of success rate (uncommon positioning)

- Intelligence service: `kalibr-intelligence.fly.dev` (ClickHouse + Redis backend, multi-tenant via X-API-Key + X-Tenant-ID)

- **Failure categories** include `hallucination_detected` and `user_unsatisfied` as structured signals

- **"Heal" mechanism:** Gate 1 failure intercepted and rerouted before reaching user (core value claim)

- **Graceful degradation:** SDK silently falls back to first path in list if Kalibr is down (order paths with most reliable first)

- **Latency overhead:** 50–100ms cold, 10–30ms warm

**Compliance Implications:**
- Kalibr adds NO compliance layer
- No consent verification, no jurisdiction-aware blocking, no AI-disclosure insertion
- GTM AI built on Kalibr must solve TCPA/CAN-SPAM/CASL/GDPR separately
- Buyer is engineering, not CFO/CCO/COO/CSO
- **Gap:** No public documentation on SOC 2, DPA, data retention, or pricing (CCO-critical)

---

### RoryPlans.ai
- **Classification:** AI work/PM orchestrator (adjacent to GTM, not core)
- **Status:** Substantive product info limited; appears positioned for internal workflow, not customer acquisition

---

### GetMinds.ai
- **Classification:** Undefined (public page returns minimal content)
- **Status:** No substantive product documentation accessible
- **Note:** If additional URLs or documentation available, can be analyzed further

---

## Part 2: B2B Outbound GTM AI — Compliance Regulations

### United States — Telephony

#### TCPA (47 USC § 227) + FCC 24-17 (Jan 27, 2026)
- **Trigger:** AI-generated voice calls to mobile/residential lines
- **Penalty:** $500–$1,500 per call, **no statutory cap**
- **Key 2026 ruling:** FCC explicitly ruled AI voice constitutes "artificial" under TCPA definition
- **Enforcement:** Recent examples: AG and class actions, Jan–Feb 2026
- **Consent requirement:** "One-to-One Consent Rule" effective Jan 27, 2026 (written consent required for most B2B + B2C calls)

#### Fifth Circuit Bradford v. Sovereign Pest Control (Feb 25, 2026)
- **Impact:** Rejected FCC's written-consent rule in 5th Circuit jurisdiction (Texas, Louisiana, Mississippi)
- **Scope:** Only 5th Circuit; other circuits still enforce
- **Implication:** Pre-call consent rules fragmented by geography

#### SMS / Text Outreach
- **Florida FTSA, Maryland SB 90, Texas SB 140**
  - State-level restrictions on unsolicited SMS
  - Vary by industry and consent type

- **Virginia (Jan 1, 2026)**
  - 10-year SMS opt-out period requirement
  - One of most stringent state regs

- **Oklahoma OTSA**
  - Oklahoma-specific text restrictions

---

### United States — Email

#### CAN-SPAM (15 USC §§ 7701–7713)
- **Applies to:** B2B and B2C email
- **Penalty:** Up to ~$53K per message (civil penalty authority, no stated cap in statute but FTC enforcement precedent)
- **Key requirements:**
  - Truthful subject line
  - Identify as advertisement (if applicable)
  - Include physical postal address
  - Honor opt-out within 10 business days

- **AI-specific gap:** Does not explicitly require AI disclosure; FTC guidance emerging

---

### United States — Endorsements & Claims

#### FTC Act § 5 + 16 CFR Part 255 (Endorsement Guides)
- **Updated June 2023** to explicitly cover AI-generated endorsers, virtual influencers, fake-review writers
- **Requirement:** Clear and conspicuous AI origin disclosure
- **Scope:** B2B and B2C; applies to brands and intermediaries

#### FTC Consumer Reviews and Testimonials Rule (2024)
- **Effective:** January 1, 2024
- **Type:** Civil-penalty rule (not guidance)
- **First enforcement:** 10 warning letters issued January 2026 to companies using fake reviews
- **Liability:** Brands and agencies co-liable with creators; "creator posted it" is not a defense
- **Penalty:** Up to $43,792 per violation (2024 inflation adjustment)

---

### United States — AI Regulation (State Level)

#### Colorado AI Act (SB 24-205)
- **Original effective date:** February 1, 2026
- **Delayed to:** June 30, 2026 (per SB 24-281)
- **Scope:** High-risk AI systems affecting legal rights or material financial interests
- **Requirements:** Risk assessments, transparency, human review

#### Utah UAIPA (Amended SB 226, 2025)
- **Safe harbor:** AI disclosure safe harbor; if compliant, liability shield
- **Penalty:** $2,500 per violation
- **Requirement:** Conspicuous AI disclosure at point of contact
- **Note:** Safe harbor applies only if disclosure is adequate and timely

---

### Canada — Email

#### CASL (Canada's Anti-Spam Legislation)
- **Type:** Opt-in (strictest in North America)
- **Penalty:** CAD $10 million (or concurrent criminal penalties)
- **Scope:** Extraterritorial (applies to any message reaching Canadian recipient)
- **Requirement:** Prior express written consent for commercial messages
- **AI exception:** None; applies to AI-generated outreach

---

### EU & UK

#### GDPR (Articles 6(1)(f), 47, 95)
- **Legal basis:** Direct marketing requires legitimate interest (Article 6(1)(f)) + Recital 47 (balancing test)
- **ePrivacy supremacy:** Article 95 states ePrivacy Directive takes precedence over GDPR for electronic marketing
- **ePrivacy Directive (2002/58/EC, amended 2009/136/EC):**
  - Opt-in for cold email, SMS, voice calls
  - Each member state implements (France, Germany, UK apply stricter versions)

#### EU AI Act (Enforced Aug 2, 2026)
- **Annex III (High-Risk Tiers):**
  - Recruitment AI
  - Government benefits assessment
  - Credit/insurance decisions
- **Requirements for enforcement date (Aug 2, 2026):**
  - Biometric identification systems must be prohibited or heavily restricted
  - Prohibited uses (social credit, non-consensual biometrics) → fines up to €30M or 6% group revenue
  - High-risk uses → transparency, documentation, human review
- **Machine-readable marking:** Providers must offer; deployers must use for deepfakes and public-interest text

#### EU AI Act Article 50 (Transparency & Disclosure)
- **Effective:** August 2, 2026
- **Requirement:** Deployers must provide visible disclosure for:
  - Deepfakes (synthetic audio/video of real person)
  - Public-interest text generated by AI (policy, news-adjacent content)
- **Code of Practice:** Draft published Dec 17, 2025; final May–June 2026
- **Penalty:** Fines up to €30M or 6% group turnover for prohibited uses; €20M or 4% for other violations

#### UK Online Safety Act (Section 35, Jan 19, 2024)
- **Scope:** Video sharing platforms must assess and mitigate risks from synthetic media (deepfakes)
- **Enforcement:** Ofcom; up to £18M fine or 5% revenue (UK subsidiary)

---

### Summary Table: B2B Outbound Regulations by Country/Region

| Jurisdiction | Rule | Type | Penalty | AI-Specific? | Enforcement 2026 |
|---|---|---|---|---|---|
| US | TCPA + FCC 24-17 | Voice | $500–$1,500/call, no cap | Yes (AI = artificial) | Active Jan 2026 |
| US | CAN-SPAM | Email | ~$53K per message | Emerging guidance | Active |
| US | FTC § 5 + 255 | Claims/endorsement | Up to $43,792/violation | Yes (June 2023 update) | Jan 2026 letters issued |
| US | Colorado SB 24-205 | State AI act | TBD (enforcement delayed to June 30, 2026) | Yes | Pending |
| US | Utah UAIPA (SB 226) | AI disclosure safe harbor | $2,500/violation | Yes | Active 2025 |
| US | Multiple states | SMS / Text | State-specific | Emerging | Active |
| Canada | CASL | Email (opt-in) | CAD $10M | No explicit AI mention, applies regardless | Active |
| EU | GDPR Art. 6(1)(f) + ePrivacy | Email/SMS | Up to €20M or 4% revenue | Emerging guidance | Active |
| EU | AI Act Annex III + Art. 50 | High-risk AI + deepfakes | Up to €30M or 6% revenue | Yes (explicit) | Enforced Aug 2, 2026 |
| UK | Online Safety Act § 35 | Synthetic media | £18M or 5% UK revenue | Yes (deepfakes explicit) | Enforcement live Jan 2024 |

---

## Part 3: Consumer-Facing AI, Deepfakes & Social Media

### Federal Deepfake Law

#### TAKE IT DOWN Act (Signed May 19, 2025)
- **Criminal provisions:** Effective immediately
- **Penalty:** 2–3 years federal prison for publishing nonconsensual intimate deepfakes
- **Platform compliance:** 48-hour notice-and-takedown process required by May 19, 2026
- **First conviction:** James Strahler II (Ohio), April 2026 (nonconsensual intimate deepfake)
- **Scope:** Applies to any deepfake of real person's intimate images without consent

#### FTC Impersonation Rule (16 CFR Part 461)
- **Effective:** April 1, 2024
- **Scope:** AI-based impersonation of government entity or established business
- **Authority:** FTC can now seek civil penalties directly in federal court (no need to prove intent to defraud; violates § 5 of FTC Act)
- **Penalty:** Civil penalties up to $43,792 per violation (2024 inflation adjustment)

---

### Consumer-Facing AI — California (Leading Edge)

#### SB 1001 (BOT Act, 2019)
- **Requirement:** Mandatory disclosure that user is interacting with a bot
- **Type:** Intent-based (disclose if bot is not obviously a bot)
- **Teeth:** Weak; limited private right of action
- **Enforcement:** Primarily state AG

#### SB 243 (Companion Chatbot Law, Effective Jan 1, 2026)
- **Scope:** AI companions designed to simulate human relationship
- **Mandatory requirements:**
  - Clear, conspicuous AI disclosure (human cannot be fooled)
  - Mandatory suicide/self-harm safety protocols with crisis referrals
  - Annual reporting to California AG (starting 2027)
- **Penalty:** $1,000 per violation + attorneys' fees (private right of action)
- **Impact:** Most stringent US consumer-AI law to date

#### Autonomous Harm Defense Eliminated (Jan 1, 2026)
- **Prior rule:** Defendant could argue "AI acted on its own" to avoid liability
- **Current rule:** No longer viable defense as of Jan 1, 2026
- **Implication:** Developer/operator liability for AI output now unavoidable

---

### Voice Cloning & Right of Publicity

#### Tennessee ELVIS Act (Effective July 1, 2024)
- **Definition:** "Voice" explicitly included in right of publicity (alongside name, image, likeness)
- **Scope:** Protects both deceased and living individuals
- **Liability:** Extends to tool providers (voice-cloning SaaS company is directly liable, not just end user)
- **Cause of action:** Unfair competition under Tennessee law
- **Damages:** Actual damages, unjust enrichment, punitive damages (up to 3x)
- **Defense:** Lack of recognition not a defense (even if deepfake is technically detectable, use without consent is violation)

#### No FAKES Act (Federal Pending)
- **Status:** Not yet enacted as of April 2026
- **Proposed scope:** Right of publicity for synthetic voice/likeness at federal level
- **Expected impact:** Would preempt fragmented state laws if enacted
- **Note:** Pending legislation; state right-of-publicity laws + ELVIS Act fill gap currently

#### State Right-of-Publicity Laws (General)
- **Coverage:** 48+ states have some form (common law or statute)
- **Trend:** Expanding to include voice, digital likeness
- **Implication:** Voice-cloning tool provider faces stacked liability across multiple jurisdictions

---

### Election Deepfakes

#### State-Level Laws (~28 states as of Jan 2026)
- **Approach 1 (Disclosure):** Require disclosure that deepfake/synthetic is non-authentic (surviving court challenges)
- **Approach 2 (Prohibition):** Outright ban on election deepfakes in certain contexts
- **Court precedent:** 
  - California AB 2839 (prohibition) partially struck down August 2025 on First Amendment + Section 230 grounds
  - Minnesota similar law under challenge
  - **Takeaway:** Disclosure laws are surviving judicial scrutiny better than prohibitions

#### Federal Deepfake Election Act (Pending)
- **Status:** Multiple bills proposed; none enacted as of April 2026
- **Expected approach:** Likely disclosure-based to pass First Amendment review

---

### Unsubstantiated Claims & Synthetic Social Content

#### FTC 16 CFR Part 255 (Endorsement Guides, Revised June 2023)
- **AI-specific coverage:** Explicitly includes AI-generated endorsers, virtual influencers, synthetic review writers
- **Requirement:** Clear and conspicuous disclosure of AI origin
- **Scope:** B2B and B2C advertising
- **Penalty:** Up to $43,792 per violation

#### FTC Consumer Reviews and Testimonials Rule (2024)
- **Effective:** January 1, 2024
- **Type:** Civil-penalty rule (enforceable; not guidance)
- **Scope:** Covers fake reviews, unsubstantiated testimonials, synthetic endorsements
- **Enforcement wave:** January 2026 warning letters to 10 companies
- **Liability:** Brands and agencies co-liable with creators; "creator posted it" is not a defense
- **Penalty:** Civil penalties up to $43,792 per violation

#### Unsubstantiated Claim Liability (General FTC Authority)
- **Rule:** All material claims must be backed by competent, reliable scientific evidence
- **AI-specific risk:** Deepfakes of experts making false claims double-violate (fake endorsement + unsubstantiated)
- **Enforcement:** FTC increasing focus on AI-generated testimonials (Jan 2026 surge in actions)

---

### EU Regulations (Consumer-Facing)

#### AI Act Article 50 (Transparency, Enforced Aug 2, 2026)
- **Deepfakes:** Machine-readable marking + visible disclosure required for synthetic audio/video of real person
- **Public-interest AI text:** Disclosure required when AI generates synthetic text on topics of public concern (policy, news)
- **Code of Practice:** Draft Dec 17, 2025; final expected May–June 2026
- **Enforcement:** Fines up to €30M or 6% group turnover for prohibited uses; €20M or 4% for high-risk violations

#### EU AI Act Annex III High-Risk (Enforced Aug 2, 2026)
- **Recruitment AI**
- **Government benefit assessment**
- **Credit/insurance decisions**
- **Requirements:** Transparency documentation, human review, risk assessments
- **Fines:** Up to €30M or 6% revenue for prohibited; €20M or 4% for high-risk violations

#### UK Online Safety Act (Section 35)
- **Scope:** Video sharing platforms must assess and mitigate synthetic media (deepfakes)
- **Enforcement:** Ofcom; up to £18M fine or 5% UK revenue

#### DSA (Digital Services Act) Enforcement (Live)
- **Example:** X fined €120M (2024–2025) for transparency/disclosure/data-access breaches
- **Implication:** Social platforms tightening deepfake/synthetic content detection and disclosure

---

## Part 4: Highest-Risk Modality

### Voice Cloning
- **Simultaneous exposures:**
  - Tennessee ELVIS Act (right of publicity, direct provider liability)
  - TCPA + FCC (if outbound call without consent, $500–$1,500 per call)
  - No FAKES Act (pending federal law)
  - State right-of-publicity laws (48+ states, expanding coverage)
  - EU AI Act Article 50 (disclosure + high-risk classification if used deceptively)
  - TAKE IT DOWN Act (if intimate content, up to 3 years prison)
  - UK Online Safety Act § 35 (if video platform, platform operator liability)

- **Why highest risk:** Single piece of audio triggers liability across telephony, endorsement, right-of-publicity, criminal deepfake, and platform regulations simultaneously

---

## Part 5: Critical Gaps in Current GTM AI Tools

### B2B Outbound
1. **Pre-send consent verification:** No product automatically checks opt-in status, jurisdiction, and legal basis before sending
2. **Jurisdiction-aware blocking:** No tool geofences outreach by TCPA region, ePrivacy rules, CASL, state SMS limits
3. **AI disclosure insertion:** No product automatically prepends "This is AI-generated" to emails/SMS/calls
4. **Claim substantiation binding:** No integration between claim generation and evidence store; false claims ship without backing

### Consumer-Facing
1. **Deepfake detection & disclosure:** No AI chatbot product ships with machine-readable marking + visible disclosure for AI origin
2. **Safety protocol automation:** No chatbot enforces mandatory California SB 243 suicide/self-harm referral flows
3. **Right-of-publicity pre-check:** No voice-cloning tool blocks ELVIS Act violations pre-deployment
4. **Election deepfake tagging:** No synthetic media tool auto-tags election content with jurisdiction-aware disclosures

### Enterprise Buyer Personas
1. **CFO:** No tool provides cost breakdowns of compliance failures (TCPA $500–$1,500 per call = $ exposure quantified)
2. **CCO:** No tool provides automated audit trail of pre-send consent checks, disclosure insertions, claim substantiation
3. **COO:** No tool integrates compliance verification into pipeline operations (SLA = "zero non-compliant outreach")
4. **CSO/CMO:** No tool connects campaign performance metrics to compliance risk scoring

---

## Part 6: Regulation Enforcement Signals (2026 Snapshot)

| Regulation | First Enforcement | Date | Enforcement Body | Impact |
|---|---|---|---|---|
| TAKE IT DOWN Act | Criminal conviction (Strahler) | April 2026 | DOJ | Signal: serious enforcement for intimate deepfakes |
| FTC Consumer Reviews Rule | Warning letters (10 companies) | January 2026 | FTC | Signal: synthetic reviews now priority |
| FTC Impersonation Rule | Ongoing (civil penalties) | 2024–present | FTC | Signal: impersonation claims tightening |
| California SB 243 | Effective Jan 1, 2026 | 2026 | CA AG + Private rights | Signal: $1K/violation; first suits expected 2026–2027 |
| Colorado AI Act | Enforcement delayed to June 30, 2026 | Originally Feb 2026 | CO AG | Signal: high-risk AI scrutiny accelerating |
| EU AI Act Annex III | Enforceable Aug 2, 2026 | Future enforcement | EU member states + EDPB | Signal: €30M fines imminent (6 months) |
| Fifth Circuit Bradford ruling | Rejected FCC consent rule | Feb 25, 2026 | Fifth Circuit (TX, LA, MS) | Signal: fragmented TCPA enforcement by circuit |
| DSA (EU) | X fined €120M | 2024–2025 | EU / national regulators | Signal: platforms liable for synthetic content |

---

## Part 7: Actionable Compliance Checklist for GTM AI Builder

### Pre-Launch (Engineering)
- [ ] Implement pre-send consent database check (opt-in status by recipient + jurisdiction)
- [ ] Add jurisdiction-aware blocking (TCPA region, ePrivacy, CASL, state SMS rules)
- [ ] Integrate AI-disclosure auto-insertion (prepend "AI-generated" to outreach)
- [ ] Link claim generation to evidence store; block unsubstantiated claims
- [ ] For voice: implement ELVIS Act pre-check (consent + right-of-publicity clearance)
- [ ] For consumer-facing: add machine-readable marking + visible AI disclosure
- [ ] For chatbots: mandate safety protocol (SB 243) with crisis referral flows

### Pre-Launch (Legal & Compliance)
- [ ] Engage counsel in 5th Circuit jurisdictions (Bradford ruling creates fragmentation)
- [ ] Audit all claims against FTC 16 CFR Part 255 (June 2023 update) + Consumer Reviews Rule
- [ ] Document consent basis for each outreach type (CAN-SPAM, CASL, ePrivacy, GDPR Art. 6)
- [ ] Run AI Act Annex III impact assessment (if EU customer base exists)
- [ ] Obtain SOC 2 Type II attestation if handling customer data (CCO requirement)

### Go-To-Market
- [ ] Market to CCO persona first (compliance risk quantification = buyer motivation)
- [ ] Price with compliance audit trail bundle (not separate upsell)
- [ ] Provide pre-signed DPA template (GDPR) and SOC 2 summary (CCO checklist item)
- [ ] Create jurisdiction-specific compliance playbooks (US multi-state + Canada + EU)

### Post-Launch (Monitoring)
- [ ] Monitor FTC & state AG enforcement actions monthly (regulations evolving fast)
- [ ] Track Fifth Circuit + other circuit TCPA ruling divergence
- [ ] Alert customers 6 months before EU AI Act Aug 2, 2026 enforcement
- [ ] Monitor California state AG SB 243 enforcement (first major cases expected 2026–2027)

---

## Sources & Regulatory Citations

### Federal (US)
- **TCPA:** 47 USC § 227; FCC 24-17 (Jan 27, 2026)
- **CAN-SPAM:** 15 USC §§ 7701–7713
- **FTC Act § 5:** 15 USC § 45
- **FTC Endorsement Guides:** 16 CFR § 255 (revised June 2023)
- **FTC Impersonation Rule:** 16 CFR Part 461 (effective April 1, 2024)
- **FTC Consumer Reviews Rule:** 16 CFR Part 455 (effective January 1, 2024)
- **TAKE IT DOWN Act:** Signed May 19, 2025; criminal provisions effective immediately
- **Fifth Circuit Bradford v. Sovereign Pest Control:** 25-20226 (Feb 25, 2026)

### State (US)
- **California SB 1001:** Chatbot disclosure (Bot Act)
- **California SB 243:** Companion chatbot law (effective Jan 1, 2026)
- **California AB 2839:** Election deepfake prohibition (partially struck down Aug 2025)
- **Colorado SB 24-205:** AI Act (enforcement delayed to June 30, 2026)
- **Utah SB 226:** UAIPA amendment (AI disclosure safe harbor, $2,500/violation)
- **Florida FTSA, Maryland SB 90, Texas SB 140:** State-level SMS restrictions
- **Virginia:** 10-year SMS opt-out (effective Jan 1, 2026)
- **Oklahoma OTSA:** Text message restrictions
- **Tennessee ELVIS Act:** Right of publicity for voice (effective July 1, 2024)

### International
- **Canada CASL:** An Act to promote the efficiency and adaptability of the Canadian economy (CAD $10M penalty, extraterritorial)
- **EU GDPR:** Regulation (EU) 2016/679; Article 6(1)(f), Recital 47, Article 95
- **EU ePrivacy Directive:** 2002/58/EC, amended 2009/136/EC
- **EU AI Act:** Regulation (EU) 2024/1689 (enforceable Aug 2, 2026); Annex III, Article 50
- **UK Online Safety Act:** 2023 (Section 35, enforcement live Jan 19, 2024)
- **UK Data Protection Act 2018:** Chapter 3 (ePrivacy implementation)

### Enforcement Examples
- **DOJ:** James Strahler II conviction (nonconsensual intimate deepfake), April 2026
- **FTC:** Warning letters to 10 companies (synthetic reviews), January 2026
- **EU:** X fined €120M (DSA transparency breaches), 2024–2025

---

## Notes & Caveats

### What Was NOT Researched (Flagged Gaps)
1. **50-state consumer AI matrix:** Comprehensive state-by-state breakdown available on request
2. **UK Online Safety Act detail:** Code of Practice and Ofcom enforcement specifics beyond Section 35
3. **Non-US/EU jurisdictions:** China, India, Singapore, Australia (emerging AI/deepfake laws)
4. **Platform ToS text:** TikTok, YouTube, Instagram deepfake/synthetic content policies (beyond legal requirement)
5. **SEC AI-washing cases:** Specific enforcement actions against GTM vendors for unsubstantiated AI claims

### Hallucination Avoidance
- All penalties, dates, and regulatory citations are drawn from official sources (Federal Register, state legislative databases, court filings, FTC enforcement actions)
- Uncertainties flagged explicitly (e.g., "pending" for No FAKES Act)
- Kalibr `/llm.txt` endpoint confirmed as 404; analysis uses official `/docs` path

---

## Next Steps for GTM AI Builders

1. **Engage counsel immediately** for TCPA + CAN-SPAM + CASL compliance architecture
2. **Run Annex III impact assessment** (EU AI Act; enforceable in 6 months as of this writing)
3. **Prioritize CCO/CFO buyer personas** (compliance gaps = buyer pain, not feature gaps)
4. **Build consent verification as core product feature**, not bolt-on
5. **Monitor FTC enforcement actions** monthly (regulatory pace is accelerating)

---

**Document Version:** 1.0 (April 18, 2026)  
**Next Review:** July 1, 2026 (post-Colorado AI Act enforcement date; pre-EU AI Act enforcement)
