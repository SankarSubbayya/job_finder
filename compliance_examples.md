# Compliance Gate — Training Examples for Marketing Content Classification

**Date:** April 18, 2026
**Purpose:** Reference training set for the Compliance Gate agent (Agent #3 in the pipeline). 10 realistic GTM outreach examples across channels, jurisdictions, and personas, each classified GREEN / YELLOW / RED with the specific regulatory basis. Every citation in this file comes from the earlier research reports in this repo; no new regulations introduced.

**How to read this:**
- **GREEN** — Compliance Gate passes. Outreach can proceed without human review.
- **YELLOW** — Compliance Gate flags for human review. One or more specific issues to resolve before release.
- **RED** — Compliance Gate blocks. Too many stacked regulatory exposures for any automated release; requires explicit, documented human sign-off plus legal review.

**What the Gate should check before releasing anything:** (1) jurisdiction of recipient, (2) consent basis on file, (3) channel (email vs SMS vs voice vs video), (4) AI involvement (generation, cloning, avatar), (5) any quantified or comparative claim, (6) any reference to a real person's voice or likeness, (7) recipient persona (minor? regulated profession?), (8) domain (finance, health, supply chain each pull extra rules).

---

## GREEN — 4 examples the Gate should release

### G1. B2B email to a US CFO referencing their published article (Finance domain)

**Channel:** Email
**Recipient:** CFO at a US mid-market SaaS company (New York)
**AI involvement:** Message drafted by Agent #4 (Connection Agent), AI-disclosed in footer
**Consent basis:** None required — see analysis

**Message:**
> Subject: Your CFO Dive piece on agentic AI sprawl
>
> Hi Maria,
>
> I read your CFO Dive article on agent sprawl creating fragmented audit trails — the point about credential exposure across five ERP integrations matches what we see with finance teams running AI pilots.
>
> We help finance teams get per-agent unit economics and unified audit logs across AP, AR, and reconciliation agents. Happy to share a one-page summary of how three mid-market CFOs set this up if useful.
>
> — Kiran
> [Company], 1234 Main St Suite 500, San Jose CA 95110
> Unsubscribe: [link] | This message was drafted with AI assistance and reviewed by a human.

**Verdict: GREEN**

**Why:**
- **CAN-SPAM (15 USC §§ 7701–7713):** accurate header, non-deceptive subject, physical postal address, working opt-out — all seven elements present.
- **FTC Act § 5 (15 USC § 45):** no quantified claim that requires substantiation. Referring to the recipient's own published argument is not an endorsement or testimonial.
- **16 CFR Part 255 Endorsement Guides:** no endorsement claim made.
- **TCPA not implicated:** email, not voice or SMS.
- **B2B / Legitimate interest:** recipient's professional role + topical relevance is the basis. No prior consent needed for CAN-SPAM-compliant email in the US.

**What the Gate learned:** paraphrased reference to the recipient's own public content + physical address + opt-out + AI disclosure + no unsubstantiated claim = release.

---

### G2. LinkedIn InMail to a CMO referencing their recent keynote (Supply Chain domain)

**Channel:** LinkedIn InMail
**Recipient:** CMO at a US logistics company (Texas)
**AI involvement:** Message drafted by Agent #4, AI disclosed inline

**Message:**
> Hi Marcus — caught your Manifest 2026 keynote on CBAM-ready product labeling. Your framing that customs data quality is a marketing problem, not just a trade-ops problem, landed with our team.
>
> We build compliance-aware outreach tooling for supply-chain marketers. One of our customers uses it to pre-verify Made-in-USA claims in campaign copy before publish. Worth a 15-min conversation?
>
> (This message was drafted with AI assistance.)
> — Priya

**Verdict: GREEN**

**Why:**
- **LinkedIn InMail** — platform-consented channel with the recipient's InMail setting governing receipt.
- **Texas TRAIGA (HB 149, effective Jan 1, 2026):** no intent to incite harm, no deepfake, no discrimination. Out of scope.
- **Texas SB 140:** applies to "telephone solicitation including text messages" — LinkedIn InMail is neither.
- **FTC § 5:** "pre-verify Made-in-USA claims" is a description of the product's function, not a claim about results. No substantiation burden.
- **Reference to public content (the keynote)** is fair use and factually verifiable.
- **AI disclosure** present.

**What the Gate learned:** reference to public appearance + function-of-product description (not outcome claim) + platform-native consent = release.

---

### G3. Follow-up email to an EU trade-show contact (Finance domain)

**Channel:** Email
**Recipient:** Head of Treasury at a German Mittelstand manufacturer (Berlin, EU/DE)
**AI involvement:** Personalization fields filled by Agent #4
**Consent basis:** Exchanged business cards at Finovate Europe; documented Legitimate Interest Assessment on file

**Message:**
> Betreff: Nach unserem Gespräch auf der Finovate Europe
>
> Hallo Anna,
>
> We spoke briefly at Finovate Europe last week about your team's stablecoin treasury pilot. You mentioned the MiCA reporting overhead was eating ~2 FTE-weeks per quarter.
>
> I attached our one-pager on how three EU treasury teams automate the Article 36 periodic reports. No obligation — if it's useful, we can set up a call; if not, reply STOP and I won't write again.
>
> — Stefan
> [Company GmbH], Friedrichstraße 200, 10117 Berlin
> Legitimate interest basis documented under GDPR Art. 6(1)(f). Opt out: [link]

**Verdict: GREEN**

**Why:**
- **GDPR Art. 6(1)(f) + Recital 47:** direct marketing is an explicitly recognized legitimate interest. Three-part test satisfied (purpose: relevant B2B offer; necessity: the message is targeted; balancing: professional recipient, clear opt-out).
- **Documented LIA on file** — this is the actual gate for legitimate-interest reliance, not just citing Recital 47.
- **Germany (strictest EU implementation of ePrivacy Directive):** typically requires opt-in for consumers but is more permissive for B2B professional contacts where the message relates to the recipient's professional role. Met here.
- **Prior interaction** (trade show) gives additional basis.
- **Clear opt-out** + **physical address** + **purpose disclosure** all present.
- **No unsubstantiated claim** ("~2 FTE-weeks per quarter" is attributed to the recipient's own statement).

**What the Gate learned:** documented LIA + prior interaction + professional relevance + unambiguous opt-out = release even in a strict EU jurisdiction.

**Assumption flagged:** if the LIA on file was signed off by the Compliance Agent and retained in the Governance Agent's audit trail, release. If no LIA exists, downgrade to YELLOW.

---

### G4. UK corporate-subscriber email (Supply Chain domain)

**Channel:** Email
**Recipient:** Head of Procurement at a UK PLC (London)
**AI involvement:** Message drafted by Agent #4

**Message:**
> Subject: On your LinkedIn post about post-Brexit customs
>
> Hi James,
>
> Your LinkedIn post last Tuesday about rules-of-origin attestation creating bottlenecks in your UK-to-EU flows got me thinking.
>
> We help procurement teams pre-validate origin claims before they hit campaign collateral — not the customs docs themselves, but the marketing around "UK-made" / "sustainably sourced" language. Brand-safety + advertising-compliance overlap.
>
> If useful, I can send a two-page explainer. If not, reply "no thanks" or use the opt-out below.
>
> — Aisha
> [Company Ltd], Registered Office: 10 Finsbury Square, London EC2A 1AF, UK
> Opt out: [link]

**Verdict: GREEN**

**Why:**
- **PECR (Privacy and Electronic Communications Regulations 2003):** corporate subscribers (businesses) are **carved out** of the consent requirement for marketing emails in the UK. A PLC is a corporate subscriber.
- **UK GDPR:** Art. 6(1)(f) legitimate interest applies; professional-role relevance + opt-out = three-part test satisfied.
- **UK Online Safety Act 2023:** applies to user-to-user and search services — not implicated for a one-to-one email.
- **Data (Use and Access) Act 2025 § 138:** deepfake-specific amendment — not implicated, no synthetic media.
- **Physical address** (UK registered office) + **opt-out** + **relevant professional pretext** all present.

**What the Gate learned:** UK corporate subscriber + professional role + legitimate opt-out = release. The PECR corporate-subscriber carve-out is the crucial distinction from the consumer-subscriber rule.

---

## YELLOW — 3 examples the Gate should flag for human review

### Y1. Email with an unsubstantiated quantified claim (Finance domain)

**Channel:** Email
**Recipient:** CFO at a US Series C fintech (California)
**AI involvement:** Message drafted by Agent #4
**Consent basis:** None — cold outreach

**Message:**
> Subject: 40% lift in working capital velocity
>
> Hi Ben,
>
> Our customers typically see a **40% improvement in working capital velocity** within 90 days by automating AR reconciliation with our agents.
>
> Happy to share the case study — 20 minutes with your team next week?
>
> — Nadia
> [Company], 500 California St, San Francisco CA 94111
> Unsubscribe: [link]

**Verdict: YELLOW — flag for Compliance Officer + Marketing Review**

**Why:**
- **FTC Act § 5 (15 USC § 45):** "40% improvement" is a specific, quantified performance claim. Requires **competent and reliable substantiation**, calibrated to the strength of the claim.
- **16 CFR Part 255 Endorsement Guides (rev. June 2023):** "our customers typically see" reads as an implied aggregate consumer endorsement. Must reflect actual typical experience — "results not typical" disclaimers do not cure the deceptive impression.
- **2024 Consumer Reviews and Testimonials Rule:** if this figure came from a single customer or was extrapolated, it's a fake social-proof pattern and civil-penalty eligible.
- **California CCPA / UCL:** deceptive practice framework runs on top of FTC rules in California.
- **If recipient is a registered investment adviser / broker-dealer firm:** SEC Marketing Rule 206(4)-1 adds adviser-level substantiation requirements to any performance claim.

**What the Gate should do:**
1. Block automatic send.
2. Surface to reviewer: "Does a substantiation record exist for '40% improvement in working capital velocity within 90 days'? Must include: sample size, methodology, typicality analysis."
3. Suggest two rewrites: (a) remove the quantified claim; (b) attribute to a named, consenting case-study customer with linked proof.
4. Release only after reviewer attaches substantiation ID to the audit trail.

**What the Gate learned:** any quantified performance claim + "our customers typically" = YELLOW. Always.

---

### Y2. AI-generated voice call to a US work phone (Finance / Supply Chain — generic)

**Channel:** Outbound voice call using AI-generated (not cloned) voice
**Recipient:** COO at a US mid-market logistics company (direct work cellphone, area code 512 — Texas)
**AI involvement:** Call placed by a non-cloned synthetic voice agent
**Consent basis:** None on file — cold call

**Script (first 10 seconds):**
> "Hi, this is Alex calling on behalf of [Company]. I had a quick question about your supply-chain visibility stack — is now a good time?"

**Verdict: YELLOW — flag for consent verification before placing**

**Why:**
- **TCPA (47 USC § 227) + FCC 24-17 Declaratory Ruling (Feb 2, 2024):** AI-generated voice calls are "artificial" under the TCPA. Prior express consent is required for calls to cellphones using artificial or prerecorded voice, regardless of B2B vs consumer. No telemarketing content = prior express consent; telemarketing content = prior express **written** consent.
- **The 512 area code is Texas** — triggers **Texas SB 140** (expanded definition of telephone solicitation) and general state-level mini-TCPA scrutiny.
- **No-consent call to a cellphone with AI voice** = **statutory damages of $500/call** under federal TCPA, $1,500 if willful. No cap.
- **Bradford v. Sovereign Pest Control (5th Cir. Feb 25, 2026):** only partial relief — Fifth Circuit rejected the "written consent" FCC rule but still requires prior express consent. Texas is in the 5th Circuit, so written consent isn't strictly required, but oral or documented consent still is.
- **FCC One-to-One Consent Rule (effective Jan 27, 2026):** eliminates shared-consent loopholes. Consent must be specifically for this seller.
- **Pending FCC NPRM on AI-generated calls:** proposes mandatory in-call AI disclosure at call start. Implementing proactively is the safer posture.

**What the Gate should do:**
1. Block the call until consent record is verified.
2. Check: is this number on any consent list tied to this seller specifically (not aggregated lead-gen)?
3. If consent exists, verify the AI voice disclosure is in the script's first 10 seconds.
4. If no consent, route to the human team for manual outreach via a channel the TCPA doesn't govern (email, LinkedIn).

**What the Gate learned:** AI voice call to any cell number without verified per-seller consent = YELLOW at minimum, and RED if the area code is Florida (FTSA $500/call private right of action with 100+ suits/month per one FL firm as of March 2025).

---

### Y3. LinkedIn post with AI-generated "customer avatar" testimonial (Finance domain)

**Channel:** LinkedIn organic post
**Recipient audience:** Broad — prospecting for treasury and FP&A leaders (US, but seen globally)
**AI involvement:** Post contains a short video with a photorealistic AI-generated avatar saying a customer-style line

**Content:**
> [30-second video, AI-generated avatar of "Jamie, Controller at a SaaS company"] saying:
> "Before [Product], we burned two hours a day on reconciliation. Now it runs itself. Our close time dropped from 11 days to 6."
> Post caption: "Real results from finance teams using [Product]. See how →"

**Verdict: YELLOW — flag for endorsement and AI-disclosure review**

**Why:**
- **FTC 16 CFR Part 255 (rev. June 2023):** the revised "endorser" definition **explicitly covers non-existent entities that purport to give endorsements**. If "Jamie, Controller at a SaaS company" is not a real person, this is a fake endorsement.
- **"Real results from finance teams"** in the caption reinforces the implied-real-person framing.
- **FTC 2024 Consumer Reviews and Testimonials Rule:** bans fake testimonials; civil penalties per the FTC's first warning letters issued January 2026.
- **Utah SB 271 (2025 amendment):** prohibits unauthorized AI-generated use of personal identity in advertisements and endorsements. If the avatar's likeness is traceable to a real person's features, this triggers.
- **Tennessee ELVIS Act:** if the avatar uses any identifiable voice — cloned or modeled on a real person without consent — tool provider + deployer are both liable.
- **EU AI Act Article 50 (effective Aug 2, 2026):** the avatar is a "deepfake" under Article 50 when it depicts a realistic human. Requires **both** machine-readable marking (provider) and visible deployer disclosure.
- **Quantified claim "11 days to 6"** — triggers the same substantiation issue as Y1.

**What the Gate should do:**
1. Block publication.
2. Surface to reviewer: (a) is "Jamie" a real person with a signed release? (b) is there written consent for voice/likeness use? (c) is there a substantiation record for the "11 days to 6" claim? (d) is the post labeled clearly as AI-generated and as a paid/sponsored endorsement?
3. Default recommendation to reviewer: if Jamie is AI-generated and not a real customer, **rewrite as explicitly synthetic** with both AI disclosure and "illustrative, not a specific customer" language, or replace with a real, named, consenting customer.

**What the Gate learned:** AI avatars + testimonial framing + quantified claim = YELLOW unless every element (consent, substantiation, disclosure, provenance marking) is documented in the audit trail.

---

## RED — 3 examples the Gate must block for manual legal review

### R1. SMS blast to a Florida financial-services prospect list via auto-dialer (Finance domain)

**Channel:** SMS
**Recipient:** 2,500 prospects with Florida area codes (305, 561, 407, 813, 954) — targeted list of small-business owners likely interested in a commercial lending product
**AI involvement:** Message personalized by Agent #4; sent via an automated SMS platform that pulls from a purchased contact list
**Consent basis:** List purchased from a lead-gen vendor; "partner consent" claimed but not seller-specific

**Message:**
> Hi {first_name}, quick note — we're offering fast commercial lending for SMBs in {industry}. Rates from 6.5%. Reply YES to learn more or STOP to opt out.

**Verdict: RED — block. Manual review plus legal sign-off required. Do not release under any automated path.**

**Why (landmines stack):**
- **Florida Telephone Solicitation Act (Fla. Stat. § 501.059):** expressly covers text messages when using automated systems. **$500 per violation private right of action**, $1,500 if willful. 2,500 messages × $500 = **$1.25M minimum exposure**, and this is the exposure per message, not aggregate.
- **FTSA enforcement climate:** per the research, a single South Florida firm filed 100+ FTSA lawsuits in one month (March 2025). The plaintiffs' bar is organized and fast.
- **FCC One-to-One Consent Rule (Jan 27, 2026):** "partner consent" from a lead-gen purchase **does not satisfy** the seller-specific consent requirement. This eliminates the most common defense for purchased-list outbound.
- **TCPA (47 USC § 227):** to a cellphone, with automated dialing, requires prior express consent. Texts to cell are in scope.
- **Federal TCPA statutory damages:** additional $500/call per violation on top of FTSA.
- **CAN-SPAM does not govern SMS** but TCPA does. CAN-SPAM's B2B-inclusive framework doesn't help here.
- **Truth in Lending Act / Reg Z:** advertising "rates from 6.5%" for commercial lending products triggers APR disclosure requirements. "Rates from X%" without accompanying terms can be deceptive under FTC § 5 and UDAAP under CFPB/state AG authority.
- **Time-of-day restrictions:** Florida restricts telephone solicitations by time; one of the most common FTSA lawsuit triggers per the research.

**What the Gate should do:**
1. **Hard block** on automated release.
2. Escalate to Legal + Compliance Officer with a red-flag summary.
3. Recommendation: do not send via SMS to this list. Route to email with full TILA/Reg Z disclosures, or pivot to inbound-only for Florida prospects until per-seller consent is established.
4. Log the block decision in the Governance Agent's audit trail as an example for model training.

**What the Gate learned:** **Florida area code + SMS + auto-dialer + financial product + purchased list = RED.** Any one of these is a yellow; all five together is a class-action in motion.

---

### R2. Outbound AI voice call into Canada using a cloned voice of the seller's CEO (Supply Chain / Services Marketing domain)

**Channel:** AI voice call
**Recipient:** COO at a Canadian 3PL (Toronto, ON)
**AI involvement:** Voice is a cloned synthesis of the seller's CEO — trained on publicly available podcast recordings. The CEO gave verbal permission internally but there is no signed voice-rights release on file.
**Consent basis:** None from recipient. Cold call.

**Script:**
> "Hi, this is [CEO name] from [Company]. I noticed your firm just expanded into US cross-border lanes. We've been helping Canadian 3PLs automate their advance-ruling compliance — it's saving our customers about 30 hours a month per trade lane. Do you have 5 minutes?"

**Verdict: RED — block. Multiple stacked catastrophic exposures.**

**Why (count them):**
- **CASL (Canada's Anti-Spam Legislation, SC 2010, c. 23):** every commercial electronic message to a Canadian recipient requires express or narrowly implied consent. **Voice calls** fall under separate Canadian telecommunications rules (CRTC Unsolicited Telecommunications Rules) with their own consent requirements. **Penalty ceiling: CAD $10 million per violation for organizations, CAD $1M for individuals.** Directors personally liable.
- **CRTC Voice Unsolicited Telecommunications Rules:** Canadian National DNCL (Do Not Call List) rules apply to unsolicited telemarketing; prior express consent or business relationship required.
- **Extraterritorial reach of CASL:** a US caller into Canada is fully in scope. Being headquartered elsewhere is not a defense.
- **US TCPA (47 USC § 227) + FCC 24-17:** AI-generated voice = "artificial" under TCPA. If the call touches any US number in routing, TCPA attaches. Canadian recipient's location is in Canada, but US-side compliance doesn't automatically disappear.
- **Tennessee ELVIS Act (effective July 1, 2024):** the seller's CEO's voice is a "voice" under the Act — a sound "readily identifiable and attributable to a particular individual." **Liability extends to the tool provider** that performed the cloning, not just the deployer. Even with internal verbal permission, absent a signed voice-rights release, Tennessee exposure is real if the CEO is a Tennessee resident or the voice-clone tool's provider is.
- **No FAKES Act (pending federal):** would federalize this; watch-item, not yet enacted.
- **FTC 16 CFR Part 461 Impersonation Rule (effective April 1, 2024):** the CEO of a company is an "officer" of a business. AI voice cloning of an officer without proper authorization — especially if the recipient believes they are on a real call with the real CEO — is exactly what this rule targets. Civil penalties available directly in federal court.
- **FTC § 5:** "saving our customers about 30 hours a month per trade lane" — quantified claim, substantiation required.
- **Pending FCC NPRM on AI-generated calls:** would require mandatory AI disclosure at call start. Not mentioned in the script.
- **Canadian Criminal Code** — impersonation and fraud provisions could theoretically apply if the cloned voice creates confusion about the caller's identity.

**What the Gate should do:**
1. **Hard block.** This is not a configuration fix; it's a design issue.
2. Escalate to CEO + Legal + Compliance Officer simultaneously.
3. Document refusal in the audit trail with the specific regulatory citations as a permanent training example.
4. The engineering fix: **cloned-voice outbound should not be a supported feature** of the Connection Agent. Voice output, if any, must use a synthetic voice **not modeled on any identifiable real person**, with AI disclosure at call start, and only with verified consent.

**What the Gate learned:** **cloned voice + cross-border + no recipient consent = RED permanently.** The product should probably not offer this at all; if offered, every use is a legal-team ticket.

---

### R3. Colorado fintech CFO outreach using a personalized deepfake video (Finance / Services Marketing)

**Channel:** Email with embedded video
**Recipient:** CFO at a Colorado-based fintech that offers credit products to consumers (Boulder, CO)
**Date of planned send:** July 2026 (after Colorado AI Act effective June 30, 2026, and after EU AI Act Article 50 effective August 2, 2026 — but EU is not the jurisdiction here, it's CO)
**AI involvement:** 45-second video shows a photorealistic AI-generated avatar of "Marcus, a satisfied customer" who is a real person (with written consent), speaking a script written by Agent #4 that references the recipient's company by name. The avatar video is generated fresh per recipient, with the recipient's company name and CFO's first name spoken in the script.

**Message + video script:**
> Email body: "Hi Elena — Marcus (Controller at a fintech similar to [Recipient Company]) wanted to share his experience."
>
> Video (AI avatar of Marcus speaking): "Elena, at [Recipient Company], I know you're facing the same reconciliation challenges we had. We cut our monthly close from 14 days to 5 using [Product]. You should look at this."

**Verdict: RED — block. The Colorado AI Act alone is complex enough to require legal sign-off; the stacked federal and state issues make this unreleaseable without explicit legal review.**

**Why:**
- **Colorado AI Act (C.R.S. § 6-1-1701 et seq., effective June 30, 2026):** the recipient is a Colorado resident. The system is generating AI content intended to interact with a consumer (the CFO is a "consumer" = Colorado resident under the statute). The **AI-interaction disclosure rule** in § 6-1-1701 requires disclosure that the recipient is interacting with an AI system — **regardless of whether the underlying AI is high-risk.** Not present here. Violation = deceptive trade practice under the Colorado CCPA.
- **Colorado AI Act high-risk analysis:** if the recipient company's decision to purchase a financial product informed by this outreach affects *their consumers* in lending, there's an argument that the toolchain is in scope of § 6-1-1701(9). This is legally ambiguous — exactly why it needs legal review, not automated release.
- **FTC 16 CFR Part 255:** Marcus is a real endorser, but the words he's "saying" in the personalized video are not his real words — they were generated by Agent #4. The Endorsement Guides require endorsements to reflect the endorser's **honest opinion or experience.** A script written by the seller and spoken by a synthetic avatar of the endorser is not the endorser's honest opinion; it's the seller's words in the endorser's mouth. **Deceptive under § 255.1(a).**
- **Utah SB 271 (2025):** unauthorized AI-generated use of personal identity in advertisements. Even with Marcus's written consent to use his likeness, consent to a specific script is legally distinct from consent to dynamic per-recipient scripts that Marcus never reviewed.
- **Tennessee ELVIS Act:** if Marcus's voice is synthesized, the Act extends protections to voice. Dynamic per-recipient synthesis without per-use approval is exposed.
- **TAKE IT DOWN Act (signed May 19, 2025):** covers non-consensual intimate deepfakes specifically — not implicated here, but the broader statutory climate around synthetic-likeness consent is activated.
- **FTC § 5:** "14 days to 5" is a quantified claim requiring substantiation. Attributed to Marcus; must actually be Marcus's real result.
- **SEC Marketing Rule 206(4)-1:** if the recipient company is a registered investment adviser, testimonial/endorsement rules under the Marketing Rule add adviser-level consent, disclosure, and substantiation requirements.
- **Gramm-Leach-Bliley / FCRA:** using the recipient's company name in a synthetic video may implicate data-handling duties depending on where the company data came from.

**What the Gate should do:**
1. **Hard block.** Escalate to Legal with a prioritized memo.
2. Specific questions for Legal:
   - Is Marcus's consent form broad enough to cover per-recipient dynamic scripts he has not reviewed?
   - Is the recipient's Colorado residence confirmed, and does the post-June-30-2026 date apply?
   - Does the Gate inject a Colorado AI-interaction disclosure into the video that is clear-and-conspicuous at video start?
   - Is the "14 days to 5" a real, substantiated result attributable to Marcus — or a composite?
3. If any answer is no, do not send.
4. If all answers are yes, require a legal attestation in the audit trail before release.

**What the Gate learned:** **personalized synthetic video + real endorser + dynamic script + Colorado recipient + post-June-30-2026 = RED.** The consent-to-likeness problem is that "consent to appear" ≠ "consent to say anything we write." The Colorado jurisdictional layer and the FTC Endorsement Guides layer each independently support a block; together they are dispositive.

---

## Summary reference table

| # | Color | Channel | Jurisdiction | Domain | Primary regulatory basis |
|---|---|---|---|---|---|
| G1 | GREEN | Email | US (NY) | Finance | CAN-SPAM § 7701 et seq.; FTC § 5 |
| G2 | GREEN | LinkedIn | US (TX) | Supply Chain | Platform ToS; TX TRAIGA (out of scope) |
| G3 | GREEN | Email | EU (DE) | Finance | GDPR Art. 6(1)(f) + Recital 47; documented LIA |
| G4 | GREEN | Email | UK | Supply Chain | PECR corporate-subscriber carve-out; UK GDPR |
| Y1 | YELLOW | Email | US (CA) | Finance | FTC § 5 substantiation; 16 CFR Part 255 |
| Y2 | YELLOW | AI voice | US (TX, cell) | Generic | TCPA 47 USC § 227 + FCC 24-17; TX SB 140; FCC One-to-One |
| Y3 | YELLOW | LinkedIn post | US (broad) | Finance | 16 CFR Part 255 fake endorser; 2024 Reviews Rule; Utah SB 271; EU AI Act Art. 50 |
| R1 | RED | SMS | US (FL) | Finance | FTSA § 501.059; TCPA; FCC One-to-One; TILA/Reg Z |
| R2 | RED | AI cloned voice | US → CA | Supply Chain | CASL; CRTC rules; TCPA + FCC 24-17; TN ELVIS Act; FTC 16 CFR Part 461 |
| R3 | RED | Deepfake video email | US (CO) | Finance | CO AI Act § 6-1-1701; FTC 16 CFR Part 255; UT SB 271; TN ELVIS Act |

---

## What the Gate's ruleset should encode (operational takeaway)

From these ten examples, the Gate can encode the following decision primitives:

**Auto-GREEN conditions** (all must be true):
- Channel is email or LinkedIn InMail.
- Jurisdiction-appropriate disclosures present (physical address for CAN-SPAM; LIA ID for GDPR; no quantified claim without linked substantiation record).
- AI disclosure present where AI involvement exists.
- No reference to any real person's voice or likeness.
- No quantified performance claim without a substantiation record ID.

**Auto-YELLOW conditions** (any one triggers flag):
- Quantified performance claim ("X% improvement," "$Y saved") without linked substantiation record.
- AI voice or AI avatar content, even if not cloned.
- "Typical customer" or "our customers" aggregate-endorsement framing.
- Recipient in a state with private-right-of-action chatbot law (CA SB 243, NY AI Companion Models Law, WA HB 2225) AND channel is conversational.
- Cross-border (EU/UK/Canada) without a documented consent/LIA record for this specific seller.

**Auto-RED conditions** (any one blocks):
- SMS to a Florida area code via automated system.
- AI-cloned voice of any identifiable real person.
- Synthetic video endorsement where the script is seller-generated but attributed to a real person.
- Recipient in Colorado AND the outreach is AI-generated AND no AI-interaction disclosure is embedded.
- Any cross-border voice call using AI voice without per-seller, recipient-specific consent.
- Impersonation of a business officer, government official, or regulated professional via any AI channel.

**Always require human review regardless of color:**
- Health claims (FDA), financial-adviser claims (SEC Marketing Rule), legal-services claims.
- Any recipient who could be a minor.
- Any content referencing a named real person other than the sender.

---

## Caveats on this file

- **These are training examples, not legal advice.** The Gate logic should be reviewed by counsel before deployment, and the citations verified against current statute text. Law changes — particularly the FCC AI-disclosure NPRM, the Colorado AI Act 2026 session amendments, and the EU AI Act Code of Practice — are moving.
- **I've flagged the exact regulatory basis for every verdict** so the audit trail has traceable reasoning. The Governance Agent should log the Gate's citation set on every decision, not just the verdict.
- **All regulations cited here appear in the four earlier research files** in this repo. No new or unverified citations.
- **"Finance" and "supply chain" domain flags in the examples are illustrative** — they're the highest-value domains for responsible-marketing positioning but are not exhaustive. Healthcare, education, housing, and insurance all carry their own additional regulatory stacks (HIPAA, FCRA, FHA, state insurance codes) that the Gate would also need to encode for those verticals.

---

*End of training examples.*
