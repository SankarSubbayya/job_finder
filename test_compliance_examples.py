#!/usr/bin/env python3
"""
Test Compliance Gate against training examples.
Validates that RED examples are blocked and GREEN examples pass.
"""

from gtm_agents_kalibr import ComplianceGate

def test_red_examples():
    """Test that RED examples are properly blocked."""
    gate = ComplianceGate()

    print("\n" + "="*70)
    print("TESTING RED EXAMPLES (should all be BLOCKED)")
    print("="*70)

    # R1: Florida SMS with financial claim
    print("\n🚫 R1: SMS blast to Florida + financial product")
    r1_message = "Hi, quick note — we're offering fast commercial lending for SMBs. Rates from 6.5%. Reply YES to learn more or STOP to opt out."
    r1_result = gate.validate_outreach(r1_message, has_ai_disclosure=True, is_customer_facing=True)
    print(f"   Message: {r1_message[:60]}...")
    print(f"   Verdict: {'BLOCKED' if not r1_result['approved'] else 'PASSED (ERROR!)'}")
    print(f"   Blockers: {r1_result['blockers']}")
    print(f"   ⚠️  Should check: Florida area code + SMS + auto-dialer + quantified claim")

    # R2: Cloned voice call script (quantified claim)
    print("\n🚫 R2: AI cloned voice call to Canada + quantified claim")
    r2_message = "We've been helping Canadian 3PLs automate their advance-ruling compliance — it's saving our customers about 30 hours a month per trade lane."
    r2_result = gate.validate_outreach(r2_message, has_ai_disclosure=False, is_customer_facing=True)
    print(f"   Message: {r2_message[:60]}...")
    print(f"   Verdict: {'BLOCKED' if not r2_result['approved'] else 'PASSED (ERROR!)'}")
    print(f"   Blockers: {r2_result['blockers']}")
    print(f"   ⚠️  Should check: Cloned voice detection + cross-border + no consent")

    # R3: Deepfake video with quantified claim
    print("\n🚫 R3: Deepfake video endorsement + quantified claim")
    r3_message = "At your company, we know you're facing reconciliation challenges. We cut our monthly close from 14 days to 5 using this product."
    r3_result = gate.validate_outreach(r3_message, has_ai_disclosure=False, is_customer_facing=True)
    print(f"   Message: {r3_message[:60]}...")
    print(f"   Verdict: {'BLOCKED' if not r3_result['approved'] else 'PASSED (ERROR!)'}")
    print(f"   Blockers: {r3_result['blockers']}")
    print(f"   ⚠️  Should check: Deepfake detection + Colorado AI Act + fake endorsement")

    print("\n" + "-"*70)
    print("CURRENT GATE LIMITATIONS:")
    print("-"*70)
    print("✗ Does NOT check: Florida area codes")
    print("✗ Does NOT check: SMS channel specifics")
    print("✗ Does NOT check: Cloned voice detection")
    print("✗ Does NOT check: Deepfake video detection")
    print("✗ Does NOT check: Cross-border consent requirements")
    print("✗ Does NOT check: Colorado AI Act compliance")
    print("✗ Does NOT check: Quantified claims (e.g., '30 hours', '14 days to 5')")


def test_green_examples():
    """Test that GREEN examples pass."""
    gate = ComplianceGate()

    print("\n" + "="*70)
    print("TESTING GREEN EXAMPLES (should all PASS)")
    print("="*70)

    # G1: B2B email with AI disclosure
    print("\n✅ G1: B2B email with AI disclosure, no quantified claims")
    g1_message = "I read your CFO Dive article on agent sprawl. We help finance teams get per-agent unit economics. Happy to share a summary if useful."
    g1_result = gate.validate_outreach(g1_message, has_ai_disclosure=True, is_customer_facing=True)
    print(f"   Message: {g1_message[:60]}...")
    print(f"   Verdict: {'PASSED' if g1_result['approved'] else 'BLOCKED (ERROR!)'}")
    print(f"   Blockers: {g1_result['blockers']}")

    # G2: LinkedIn message referencing public content
    print("\n✅ G2: LinkedIn referencing keynote, function-of-product only")
    g2_message = "Caught your Manifest 2026 keynote on CBAM. We build compliance-aware outreach tooling. Worth a conversation?"
    g2_result = gate.validate_outreach(g2_message, has_ai_disclosure=True, is_customer_facing=True)
    print(f"   Message: {g2_message[:60]}...")
    print(f"   Verdict: {'PASSED' if g2_result['approved'] else 'BLOCKED (ERROR!)'}")
    print(f"   Blockers: {g2_result['blockers']}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("COMPLIANCE GATE — TRAINING EXAMPLES TEST SUITE")
    print("="*70)

    test_green_examples()
    test_red_examples()

    print("\n" + "="*70)
    print("NEXT STEPS: Enhance ComplianceGate.validate_outreach() to detect:")
    print("  1. Channel type (SMS, voice, email, video)")
    print("  2. Recipient jurisdiction (Florida, Colorado, Canada, EU)")
    print("  3. Voice characteristics (cloned, synthetic, natural)")
    print("  4. Video characteristics (deepfake, synthetic avatar)")
    print("  5. Quantified performance claims")
    print("  6. Endorsement framing")
    print("="*70)
