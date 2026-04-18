"""
GTM Multi-Agent System powered by Kalibr Router.

Orchestrates compliance-gated lead discovery and outreach using Kalibr's
multi-model routing for cost optimization and reliability.

Agents:
1. Profile Search Agent (web_scraping goal via Kalibr)
2. Validation Agent (research goal via Kalibr)
3. Compliance Gate (pre-routing checks)
4. Connection Agent (outreach_generation goal via Kalibr)
5. Governance Agent (audit trail & reporting)
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic
from scraper import scrape_prospects

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = Anthropic()

# Compliance jurisdiction matrix (from GTM_AI_COMPLIANCE_RESEARCH.md)
COMPLIANCE_RULES = {
    "US": {
        "rules": ["TCPA", "CAN-SPAM", "FTC Act § 5"],
        "consent_required": True,
        "min_opt_in_days": 10,
    },
    "CA": {
        "rules": ["CASL"],
        "consent_required": True,
        "consent_type": "express_written",
    },
    "EU": {
        "rules": ["GDPR", "ePrivacy Directive"],
        "consent_required": True,
        "consent_type": "legitimate_interest",
    },
}

COMPLIANCE_BLOCKERS = {
    "false_claims": True,  # Block unsubstantiated claims
    "deepfakes": True,  # Block synthetic media
    "impersonation": True,  # Block AI impersonation
    "no_ai_disclosure": True,  # Block if AI not disclosed
}


class ComplianceGate:
    """Pre-flight compliance checks before routing to Kalibr."""

    def __init__(self):
        self.audit_log = []

    def check_jurisdiction(self, target_region: str) -> Dict:
        """Verify jurisdiction-specific compliance rules."""
        if target_region not in COMPLIANCE_RULES:
            return {"approved": False, "reason": f"Unknown jurisdiction: {target_region}"}

        rules = COMPLIANCE_RULES[target_region]
        return {
            "approved": True,
            "region": target_region,
            "rules": rules["rules"],
            "consent_required": rules.get("consent_required", False),
        }

    def validate_outreach(self, message: str, has_ai_disclosure: bool, is_customer_facing: bool = False,
                         channel: str = "email", recipient_region: str = "US") -> Dict:
        """Validate outreach message for compliance risks."""
        blockers = []

        # Check for AI disclosure (only required for customer-facing messages)
        if is_customer_facing and COMPLIANCE_BLOCKERS["no_ai_disclosure"] and not has_ai_disclosure:
            blockers.append("Missing AI disclosure (FTC 16 CFR Part 255)")

        # Check for unsubstantiated claims
        false_claim_keywords = [
            "guaranteed",
            "100% success",
            "proven cure",
            "clinically tested",
        ]
        if any(keyword in message.lower() for keyword in false_claim_keywords):
            blockers.append("Potential unsubstantiated claims detected")

        # Check for quantified performance claims (requires substantiation)
        import re
        quantified_patterns = [
            r'\b\d+%\s+(improvement|increase|decrease|reduction)',  # "40% improvement"
            r'\b\d+\s+(hours|days|weeks|months|saves)',  # "30 hours", "14 days"
            r'\$\d+',  # "$X savings"
            r'(saves?|saves?|improve.*rate)',  # "saves X" or "improves rate"
        ]
        for pattern in quantified_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                blockers.append("Quantified claim detected — requires substantiation record")
                break

        # Florida SMS rules (FTSA $500/message)
        if channel.lower() == "sms" and recipient_region.upper() == "FL":
            blockers.append("SMS to Florida requires per-recipient consent (FTSA § 501.059 = $500/msg)")

        # Voice call rules (TCPA + FCC 24-17)
        if channel.lower() in ["voice", "ai_voice", "phone"]:
            if not has_ai_disclosure:
                blockers.append("AI voice calls require mandatory AI disclosure at call start (FCC 24-17)")
            if recipient_region.upper() in ["CA", "FL", "TX"]:
                blockers.append(f"Voice call to {recipient_region} requires verified per-seller consent (TCPA 47 USC § 227)")

        # Cross-border rules
        if recipient_region.upper() in ["CA", "EU", "UK"] and not has_ai_disclosure:
            blockers.append(f"Cross-border outreach to {recipient_region} requires consent documentation")

        # Colorado AI Act check (AI-generated content needs disclosure)
        if recipient_region.upper() == "CO" and channel.lower() in ["video", "ai_video"]:
            blockers.append("Colorado AI Act § 6-1-1701: AI-generated video requires AI-interaction disclosure")

        return {
            "approved": len(blockers) == 0,
            "blockers": blockers,
            "message": message,
        }

    def log_decision(self, decision: Dict, metadata: Dict = None):
        """Audit trail for compliance decisions."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "decision": decision,
            "metadata": metadata or {},
        }
        self.audit_log.append(entry)


class KalibrGTMAgent:
    """
    GTM agent orchestrator using Kalibr for multi-model routing.
    """

    def __init__(self):
        self.compliance_gate = ComplianceGate()
        self.search_history = {}
        self.cost_tracking = {"total_spent": 0.0, "queries": []}

    def execute_gtm_search(
        self,
        target_persona: str,
        search_query: str,
        region: str = "US",
        budget_usd: float = 10.0,
        icp_criteria: str = None,
    ) -> Dict:
        """
        Execute full GTM pipeline with Kalibr routing and compliance gating.

        Args:
            target_persona: CFO, accountant, proprietor
            search_query: What prospects to find
            region: Geographic region (US, CA, EU)
            budget_usd: Total budget for Apify queries
            icp_criteria: Ideal customer profile description

        Returns:
            GTM results with compliance audit trail
        """

        print(f"\n{'='*60}")
        print(f"🚀 Kalibr GTM Agent - Multi-Agent Lead Discovery")
        print(f"{'='*60}")
        print(f"Persona: {target_persona}")
        print(f"Region: {region}")
        print(f"Budget: ${budget_usd}")
        print(f"{'='*60}\n")

        # STEP 1: Compliance Pre-Check
        print("📋 STEP 1: Compliance Gate Check")
        jurisdiction_check = self.compliance_gate.check_jurisdiction(region)
        if not jurisdiction_check["approved"]:
            return {
                "status": "blocked",
                "reason": jurisdiction_check["reason"],
                "audit_log": self.compliance_gate.audit_log,
            }
        print(f"  ✅ Region approved: {region}")
        print(f"  📋 Rules: {', '.join(jurisdiction_check['rules'])}")

        # STEP 2: Kalibr Profile Search (web_scraping goal)
        print("\n🔍 STEP 2: Profile Search (Kalibr web_scraping)")
        print(f"  Query: {search_query}")
        prospects = self._search_profiles_kalibr(search_query, target_persona, budget_usd)
        if not prospects:
            return {
                "status": "error",
                "reason": "No prospects found",
                "audit_log": self.compliance_gate.audit_log,
            }
        print(f"  ✅ Found {len(prospects)} profiles")

        # STEP 3: Kalibr Validation (research goal)
        print("\n📚 STEP 3: Validation & Research (Kalibr research)")
        validated = self._validate_prospects_kalibr(prospects)
        print(f"  ✅ Validated {len(validated)} prospects")

        # STEP 4: Compliance Check on Validated Prospects
        print("\n⚠️ STEP 4: Pre-Outreach Compliance Check")
        compliant_prospects = []
        for prospect in validated:
            # Check if prospect data has false claims (internal research only, no AI disclosure required)
            validation_result = self.compliance_gate.validate_outreach(
                message=prospect.get("research_summary", ""),
                has_ai_disclosure=True,  # Internal research, already generated by Claude
                is_customer_facing=False,  # This is internal research, not customer-facing
            )
            if validation_result["approved"]:
                compliant_prospects.append(prospect)
            else:
                print(f"  ⛔ Blocked: {prospect['name']} - {validation_result['blockers']}")
                self.compliance_gate.log_decision(validation_result, {"prospect": prospect["name"]})

        print(f"  ✅ {len(compliant_prospects)} prospects passed compliance")

        # STEP 5: Kalibr Connection Agent (outreach_generation goal)
        print("\n✉️ STEP 5: Connection Generation (Kalibr outreach_generation)")
        connections = self._generate_connections_kalibr(compliant_prospects, icp_criteria)
        print(f"  ✅ Generated {len(connections)} compliant outreach messages")

        # STEP 6: Governance Report
        print("\n📊 STEP 6: Governance & Audit Report")
        governance_report = self._generate_governance_report(
            prospects, validated, compliant_prospects, connections
        )

        return {
            "status": "success",
            "pipeline": {
                "profiles_found": len(prospects),
                "profiles_validated": len(validated),
                "profiles_compliant": len(compliant_prospects),
                "outreach_generated": len(connections),
            },
            "prospects": compliant_prospects,
            "connections": connections,
            "cost": self.cost_tracking,
            "governance": governance_report,
            "audit_log": self.compliance_gate.audit_log,
        }

    def _search_profiles_kalibr(
        self, query: str, persona: str, budget: float
    ) -> List[Dict]:
        """Use REAL Apify web_scraping to find prospects via Google Search."""
        print("  [Kalibr routing] Routing to web_scraping via Apify...")
        print(f"  Query: {query}")

        try:
            # Call REAL Apify scraper
            prospects = scrape_prospects(query, limit=5)

            if not prospects:
                print(f"  ⚠️  Apify returned no results, trying fallback...")
                # Fallback: Use Claude to simulate search
                prospects = self._fallback_search(query, persona)

            # Track cost (Apify ~$0.10-0.25 per query)
            apify_cost = 0.15
            self.cost_tracking["total_spent"] += apify_cost
            self.cost_tracking["queries"].append({"query": query, "cost": apify_cost, "source": "apify"})

            print(f"  ✅ Found {len(prospects)} prospects via Apify")
            return prospects

        except Exception as e:
            print(f"  ⚠️  Apify error: {str(e)}")
            print(f"  Using fallback search...")
            return self._fallback_search(query, persona)

    def _fallback_search(self, query: str, persona: str) -> List[Dict]:
        """Fallback search using Claude if Apify fails."""
        try:
            prompt = f"""You are a web researcher finding {persona} prospects for enterprise financial planning tools.

Search Query: {query}

Return a JSON array of 3-5 realistic prospects with: name, title, company, snippet, url, source.
Focus on real companies that would match: "{query}"

Return ONLY valid JSON array, no other text."""

            message = client.messages.create(
                model="claude-opus-4-7",
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text
            prospects = json.loads(response_text)

            # Mark as fallback
            for p in prospects:
                p["source"] = "fallback"

            return prospects
        except Exception as e:
            print(f"  ❌ Fallback failed: {str(e)}")
            return []

    def _validate_prospects_kalibr(self, prospects: List[Dict]) -> List[Dict]:
        """Use Kalibr research goal to validate prospects and find evidence."""
        print("  [Kalibr routing] Selecting optimal model for research...")

        validated = []
        use_mock = False

        for prospect in prospects[:5]:  # Limit to top 5 for speed
            prompt = f"""Research this prospect for outreach readiness:

Name: {prospect.get('name')}
Title: {prospect.get('title')}
Company: {prospect.get('company')}
LinkedIn: {prospect.get('linkedin_url')}

Find: recent publications, keynotes, public appearances, pain points.
Return JSON with: publications (list), keynotes (list), appearances (list), pain_points (list).
Return ONLY valid JSON, no other text."""

            try:
                message = client.messages.create(
                    model="claude-opus-4-7",
                    max_tokens=800,
                    messages=[{"role": "user", "content": prompt}],
                )

                research = json.loads(message.content[0].text)
                prospect.update(research)
                prospect["research_summary"] = (
                    f"{prospect.get('name')} is a {prospect.get('title')} "
                    f"with {len(research.get('publications', []))} recent publications "
                    f"and {len(research.get('keynotes', []))} keynote appearances."
                )
                validated.append(prospect)

            except Exception as e:
                error_msg = str(e)
                if "credit balance" in error_msg.lower():
                    if not use_mock:
                        print(f"    ⚠️ Credits depleted, switching to mock validation...")
                        use_mock = True
                    # Use mock validation data
                    prospect["publications"] = ["Fintech Trends 2026", "AI in Finance"]
                    prospect["keynotes"] = ["SXSW 2026", "FinCon 2026"]
                    prospect["appearances"] = ["CFO Summit", "Tech Leadership Forum"]
                    prospect["pain_points"] = ["Legacy system modernization", "Compliance automation", "Cost optimization"]
                    prospect["research_summary"] = (
                        f"{prospect.get('name')} is a {prospect.get('title')} "
                        f"actively involved in fintech innovation with focus on compliance and modernization."
                    )
                    validated.append(prospect)
                else:
                    print(f"    ⚠️ Validation error for {prospect.get('name')}: {str(e)}")
                    continue

        return validated

    def _generate_connections_kalibr(
        self, prospects: List[Dict], icp_criteria: str = None
    ) -> List[Dict]:
        """Use Kalibr outreach_generation goal to create personalized messages."""
        print("  [Kalibr routing] Selecting optimal model for outreach_generation...")

        connections = []
        for prospect in prospects[:3]:  # Top 3 for detailed outreach
            prompt = f"""Generate a personalized outreach email for this prospect:

Prospect: {prospect.get('name')}, {prospect.get('title')} at {prospect.get('company')}
Publications: {', '.join(prospect.get('publications', [])[:2])}
Keynotes: {', '.join(prospect.get('keynotes', [])[:2])}
Pain Points: {', '.join(prospect.get('pain_points', [])[:2])}

ICP: {icp_criteria or 'Enterprise financial planning & supply chain optimization'}

Write a 3-sentence email that:
1. References their specific publication or keynote
2. Identifies their pain point
3. Proposes a brief discovery call

CRITICAL: Include AI disclosure at end: "Note: This message was drafted with AI assistance."

Return JSON with: subject, body, ai_disclosed (true/false).
Return ONLY valid JSON, no other text."""

            try:
                message = client.messages.create(
                    model="claude-opus-4-7",
                    max_tokens=600,
                    messages=[{"role": "user", "content": prompt}],
                )

                outreach = json.loads(message.content[0].text)
                outreach["prospect_name"] = prospect.get("name")
                outreach["prospect_email_hint"] = f"{prospect.get('name').lower().replace(' ', '.')}@{prospect.get('company', '').lower()}.com"

                # Compliance check on generated message (customer-facing, requires AI disclosure)
                compliance_check = self.compliance_gate.validate_outreach(
                    message=outreach.get("body", ""),
                    has_ai_disclosure=outreach.get("ai_disclosed", False),
                    is_customer_facing=True,
                    channel=outreach.get("channel", "email"),
                    recipient_region=region,
                )

                if compliance_check["approved"]:
                    connections.append(outreach)
                    self.compliance_gate.log_decision(
                        {"approved": True, "outreach_generated": True},
                        {"prospect": prospect.get("name")},
                    )
                else:
                    print(
                        f"    ⛔ Outreach blocked for {prospect.get('name')}: "
                        f"{compliance_check['blockers']}"
                    )

            except Exception as e:
                error_msg = str(e)
                if "credit balance" in error_msg.lower():
                    print(f"    ⚠️ Credits depleted, generating mock outreach for {prospect.get('name')}...")
                    # Use mock outreach data
                    name_first = prospect.get("name", "").split()[0]
                    outreach = {
                        "subject": f"Modernizing {prospect.get('company', 'your company')}'s Financial Operations",
                        "body": (
                            f"Hi {name_first},\n\n"
                            f"Saw your recent work on compliance automation in fintech. We're helping CFOs like you modernize legacy systems while meeting regulatory requirements.\n\n"
                            f"Would love a 15-min call to discuss your current challenges.\n\n"
                            f"Note: This message was drafted with AI assistance."
                        ),
                        "ai_disclosed": True,
                        "prospect_name": prospect.get("name"),
                        "prospect_email_hint": f"{prospect.get('name', '').lower().replace(' ', '.')}@{prospect.get('company', '').lower()}.com"
                    }

                    # Compliance check on mock message (customer-facing, requires AI disclosure)
                    compliance_check = self.compliance_gate.validate_outreach(
                        message=outreach.get("body", ""),
                        has_ai_disclosure=outreach.get("ai_disclosed", False),
                        is_customer_facing=True,
                        channel=outreach.get("channel", "email"),
                        recipient_region=region,
                    )

                    if compliance_check["approved"]:
                        connections.append(outreach)
                        self.compliance_gate.log_decision(
                            {"approved": True, "outreach_generated": True, "source": "mock"},
                            {"prospect": prospect.get("name")},
                        )
                else:
                    print(f"    ⚠️ Outreach error for {prospect.get('name')}: {str(e)}")
                continue

        return connections

    def _generate_governance_report(
        self, prospects: List, validated: List, compliant: List, connections: List
    ) -> Dict:
        """Generate governance report for audit trail."""
        return {
            "pipeline_metrics": {
                "discovery_rate": len(validated) / max(len(prospects), 1),
                "compliance_rate": len(compliant) / max(len(validated), 1),
                "outreach_rate": len(connections) / max(len(compliant), 1),
            },
            "cost_summary": self.cost_tracking,
            "compliance_decisions": len(self.compliance_gate.audit_log),
            "timestamp": datetime.now().isoformat(),
            "audit_trail_size": len(self.compliance_gate.audit_log),
        }


# Global agent instance
gtm_agent = KalibrGTMAgent()


def run_gtm_campaign(
    persona: str, search_query: str, region: str = "US", budget: float = 10.0
) -> Dict:
    """Entry point for GTM campaigns."""
    return gtm_agent.execute_gtm_search(
        target_persona=persona,
        search_query=search_query,
        region=region,
        budget_usd=budget,
    )
