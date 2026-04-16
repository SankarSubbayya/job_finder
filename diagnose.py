#!/usr/bin/env python3
"""Comprehensive diagnosis of Job Finder issues."""

import os
import json
from pathlib import Path

def check_env():
    """Check environment variables."""
    print("1️⃣  CHECKING ENVIRONMENT VARIABLES")
    print("=" * 60)

    if not Path('.env').exists():
        print("❌ .env file not found!")
        return False

    with open('.env') as f:
        content = f.read()

    has_token = 'APIFY_TOKEN=' in content
    has_key = 'YOU_API_KEY=' in content

    print(f"  ✓ .env exists")
    print(f"  {'✓' if has_token else '❌'} APIFY_TOKEN configured")
    print(f"  {'✓' if has_key else '⚠️'} YOU_API_KEY configured (optional)")

    # Check if using placeholders
    if 'your_apify_token' in content.lower():
        print("  ❌ APIFY_TOKEN is still a placeholder!")
        print("     Action: Add your real token to .env")
        return False

    return True


def check_dependencies():
    """Check if all dependencies are installed."""
    print("\n2️⃣  CHECKING DEPENDENCIES")
    print("=" * 60)

    deps = ['pdfplumber', 'apify_client', 'requests', 'dotenv']
    all_ok = True

    for dep in deps:
        try:
            __import__(dep)
            print(f"  ✓ {dep}")
        except ImportError:
            print(f"  ❌ {dep} NOT installed")
            all_ok = False

    if not all_ok:
        print("\n  Fix: Run 'uv sync'")

    return all_ok


def check_resume_parsing():
    """Check resume parsing with a test PDF."""
    print("\n3️⃣  CHECKING RESUME PARSING")
    print("=" * 60)

    from pdf_parser import parse_resume

    # Try to find a test resume
    resume_files = list(Path('.').glob('*.pdf'))

    if not resume_files:
        print("  ⚠️  No PDF files found for testing")
        return None

    try:
        resume_file = resume_files[0]
        print(f"  Testing with: {resume_file.name}")

        result = parse_resume(str(resume_file))

        print(f"  ✓ Parsing successful")
        print(f"    - Title: {result['title']}")
        print(f"    - Skills: {len(result['skills'])} found")
        print(f"    - Location: {result['location']}")
        print(f"    - Level: {result['level']}")

        if not result['title'] or result['title'] == 'Software Engineer':
            print("  ⚠️  Title extraction might be incorrect")
            return False

        if not result['skills']:
            print("  ❌ No skills extracted!")
            return False

        return True

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def check_latest_results():
    """Check latest search results."""
    print("\n4️⃣  CHECKING LATEST SEARCH RESULTS")
    print("=" * 60)

    if not Path('job_matches.json').exists():
        print("  ❌ No results file found")
        print("     Action: Run 'python impl.py --resume your.pdf' first")
        return False

    with open('job_matches.json') as f:
        data = json.load(f)

    total = data.get('total_matches', 0)
    jobs = data.get('matched_jobs', [])

    print(f"  Total matches: {total}")
    print(f"  Jobs in results: {len(jobs)}")

    if not jobs:
        print("  ❌ No jobs in results!")
        print("     Possible causes:")
        print("       - Apify not returning data")
        print("       - All jobs scored below MIN_JOB_SCORE")
        print("       - No skills extracted from resume")
        return False

    # Check job titles
    titles = sum(1 for j in jobs if j.get('title', '').strip())
    print(f"  Jobs with titles: {titles}/{len(jobs)}")

    if titles == 0:
        print("  ❌ All jobs missing titles!")
        print("     This means Apify response structure is different")
        print("     Run: python debug_scraper.py")
        return False

    # Check scores
    avg_score = sum(j.get('match_score', 0) for j in jobs) / len(jobs) if jobs else 0
    print(f"  Average match score: {avg_score*100:.0f}%")

    if avg_score < 0.3:
        print("  ⚠️  Low average scores - might need skill improvements")

    return True


def main():
    """Run all diagnostics."""
    print("\n" + "🔍 JOB FINDER DIAGNOSTIC".center(60, "="))
    print()

    results = {
        'Environment': check_env(),
        'Dependencies': check_dependencies(),
        'Resume Parsing': check_resume_parsing(),
        'Search Results': check_latest_results(),
    }

    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)

    for check, result in results.items():
        if result is None:
            status = "⚠️  SKIPPED"
        elif result:
            status = "✓ PASS"
        else:
            status = "❌ FAIL"
        print(f"  {status}: {check}")

    print("\n" + "=" * 60)

    if all(v for v in results.values() if v is not None):
        print("✅ All checks passed!")
    else:
        print("❌ Some checks failed. See above for details.")

    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
