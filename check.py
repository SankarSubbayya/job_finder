#!/usr/bin/env python3
"""Verification script to check Job Finder Agent setup."""

import sys
import os
from pathlib import Path


def check_python_version():
    """Check Python version."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ✗ Python 3.8+ required, found {version.major}.{version.minor}")
        return False


def check_dependencies():
    """Check if all required packages are installed."""
    print("\n📦 Checking dependencies...")
    required = ["pdfplumber", "apify_client", "requests", "dotenv"]
    missing = []

    for package in required:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (missing)")
            missing.append(package)

    if missing:
        print(f"\n  Install missing packages:")
        print(f"  pip install -r requirements.txt")
        return False
    return True


def check_env_file():
    """Check .env file and API keys."""
    print("\n🔑 Checking environment configuration...")
    env_path = Path(".env")

    if not env_path.exists():
        print("  ✗ .env file not found")
        return False

    print("  ✓ .env file found")

    # Check for API tokens
    with open(env_path) as f:
        content = f.read()

    has_apify = "APIFY_TOKEN=apify_api_" in content
    has_you = "YOU_API_KEY=ydc_" in content or "YOU_API_KEY=your_" in content

    if has_apify:
        print("  ✓ APIFY_TOKEN configured")
    else:
        print("  ⚠ APIFY_TOKEN not configured (required)")
        return False

    if has_you:
        print("  ✓ YOU_API_KEY configured (optional)")
    else:
        print("  ⚠ YOU_API_KEY not configured (optional)")

    return True


def check_files():
    """Check if all required files exist."""
    print("\n📁 Checking project structure...")
    required_files = [
        "impl.py",
        "pdf_parser.py",
        "matcher.py",
        "enricher.py",
        "formatter.py",
        "config.py",
        "SKILL.md",
        "README.md",
        "requirements.txt",
        "scrapers/apify_client.py",
        "scrapers/linkedin.py",
        "scrapers/indeed.py",
        "scrapers/hackernews.py",
    ]

    missing = []
    for file in required_files:
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (missing)")
            missing.append(file)

    return len(missing) == 0


def check_syntax():
    """Check Python syntax of main files."""
    print("\n✨ Checking Python syntax...")
    import py_compile

    files = [
        "impl.py",
        "pdf_parser.py",
        "matcher.py",
        "enricher.py",
        "formatter.py",
        "config.py",
    ]

    all_valid = True
    for file in files:
        try:
            py_compile.compile(file, doraise=True)
            print(f"  ✓ {file}")
        except py_compile.PyCompileError as e:
            print(f"  ✗ {file}: {e}")
            all_valid = False

    return all_valid


def check_imports():
    """Test that imports work."""
    print("\n🔗 Checking imports...")
    try:
        from dotenv import load_dotenv
        print("  ✓ dotenv import")
        load_dotenv()

        from config import APIFY_TOKEN, YOU_API_KEY
        print("  ✓ config import")

        if APIFY_TOKEN:
            print("  ✓ APIFY_TOKEN loaded from .env")
        else:
            print("  ✗ APIFY_TOKEN not loaded")
            return False

        from pdf_parser import parse_resume
        print("  ✓ pdf_parser import")

        from matcher import rank_jobs
        print("  ✓ matcher import")

        from enricher import enrich_with_company_info
        print("  ✓ enricher import")

        from formatter import format_job_results
        print("  ✓ formatter import")

        return True

    except Exception as e:
        print(f"  ✗ Import error: {e}")
        return False


def main():
    """Run all checks."""
    print("=" * 60)
    print("🎯 Job Finder Agent - Setup Verification")
    print("=" * 60)

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment", check_env_file),
        ("Project Structure", check_files),
        ("Python Syntax", check_syntax),
        ("Module Imports", check_imports),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)

    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
        if not result:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n✅ All checks passed! Application is ready to use.")
        print("\nRun the Job Finder with:")
        print("  python impl.py --resume path/to/resume.pdf")
        return 0
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
