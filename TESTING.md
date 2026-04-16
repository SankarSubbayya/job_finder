# 🧪 Job Finder Agent - Testing Guide

## Testing Levels

### 1️⃣ Setup Verification (Fastest)
### 2️⃣ Unit Testing (Individual Components)
### 3️⃣ Integration Testing (End-to-End)
### 4️⃣ Manual Testing (Real API Calls)
### 5️⃣ OpenClaw Skill Testing (In Chat)

---

## Level 1: Setup Verification ⚡

**Time:** 30 seconds | **No API calls**

### Run the Check Script
```bash
python check.py
```

**Expected Output:**
```
============================================================
🎯 Job Finder Agent - Setup Verification
============================================================
✓ PASS: Python Version
✓ PASS: Dependencies
✓ PASS: Environment
✓ PASS: Project Structure
✓ PASS: Python Syntax
✓ PASS: Module Imports
============================================================
✅ All checks passed! Application is ready to use.
```

**What It Tests:**
- ✓ Python 3.8+ installed
- ✓ All dependencies available
- ✓ .env file configured
- ✓ All project files present
- ✓ Python syntax valid
- ✓ Modules import correctly
- ✓ API keys loaded from .env

---

## Level 2: Unit Testing 🔬

**Time:** 2-3 minutes | **No API calls**

### Test PDF Parser
```bash
python3 << 'EOF'
from pdf_parser import extract_skills, extract_job_title, extract_location, extract_experience_level

# Test skill extraction
text = "I have Python, AWS, Docker, and React experience"
skills = extract_skills(text)
print(f"✓ Skills extracted: {skills}")
assert "Python" in skills

# Test job title extraction
text = "Senior Python Engineer at Google"
title = extract_job_title(text)
print(f"✓ Title extracted: {title}")

# Test location extraction
text = "Based in San Francisco, CA"
location = extract_location(text)
print(f"✓ Location extracted: {location}")

# Test experience level
text = "5 years of experience as a senior developer"
level = extract_experience_level(text)
print(f"✓ Level extracted: {level}")

print("\n✅ PDF Parser tests passed!")
EOF
```

### Test Job Matcher
```bash
python3 << 'EOF'
from matcher import score_job_match, rank_jobs, deduplicate_jobs

# Test job scoring
resume_info = {
    "title": "Python Engineer",
    "skills": ["Python", "AWS", "Docker"],
    "location": "San Francisco, CA",
    "level": "senior"
}

job = {
    "title": "Senior Python Engineer",
    "company": "Google",
    "location": "San Francisco, CA",
    "description": "Looking for Python developer with AWS experience",
    "url": "https://example.com"
}

score = score_job_match(job, resume_info)
print(f"✓ Job match score: {score:.2f} (should be > 0.5)")
assert score > 0.5

# Test deduplication
jobs = [
    {"title": "Python Dev", "company": "Google"},
    {"title": "Python Dev", "company": "Google"},  # Duplicate
    {"title": "Python Dev", "company": "Meta"}
]

unique = deduplicate_jobs(jobs)
print(f"✓ Deduplicated: {len(jobs)} → {len(unique)} jobs")
assert len(unique) == 2

print("\n✅ Matcher tests passed!")
EOF
```

### Test Formatter
```bash
python3 << 'EOF'
from formatter import format_single_job, _get_score_bar

# Test job formatting
job = {
    "title": "Senior Python Engineer",
    "company": "Google",
    "location": "San Francisco, CA",
    "match_score": 0.92,
    "description": "Build ML systems at scale",
    "url": "https://linkedin.com/jobs/123"
}

formatted = format_single_job(job, rank=1)
print(f"✓ Formatted job:\n{formatted}")

# Test score bar
bar = _get_score_bar(0.75)
print(f"✓ Score bar (75%): {bar}")
assert "█" in bar

print("\n✅ Formatter tests passed!")
EOF
```

---

## Level 3: Integration Testing 🔗

**Time:** 5-10 minutes | **Uses real APIs**

### Create a Test Resume
Create `test_resume.txt`:
```
JOHN DOE
San Francisco, CA

EXPERIENCE
Senior Python Engineer at TechCorp (2020-2024)
- Developed Python applications
- AWS and Docker expertise
- 5+ years experience

SKILLS
Python, JavaScript, AWS, Docker, Kubernetes, React, SQL, Machine Learning
```

Convert to PDF (or use an existing one).

### Run Full Pipeline
```bash
python impl.py --resume test_resume.pdf
```

**Expected Output:**
```
🔍 Job Finder Agent Starting...

📄 Parsing resume...
  ✓ Extracted profile:
    - Title: Senior Python Engineer
    - Location: San Francisco, CA
    - Level: senior
    - Skills: 8 found

🕷️  Scraping job boards (LinkedIn, Indeed, HackerNews)...
  ✓ LinkedIn: 50 jobs
  ✓ Indeed: 45 jobs
  ✓ HackerNews: 12 jobs

🔄 Deduplicating results...
  ✓ 95 unique jobs after deduplication

⭐ Ranking jobs by match...
  ✓ 18 jobs meet minimum score threshold

🏢 Enriching with company information...
  ✓ Company info added to top matches

✨ Formatting results...

============================================================
✅ Job Finder Complete!
============================================================

📋 Your Job Search Summary
[... summary output ...]

🎯 Found 18 matching jobs (showing top 10):
[... job listings ...]

💾 Results saved to job_matches.json
```

### Verify JSON Output
```bash
python3 << 'EOF'
import json

with open("job_matches.json") as f:
    data = json.load(f)

print(f"✓ Total matches: {data['total_matches']}")
print(f"✓ Resume title: {data['resume_info']['title']}")
print(f"✓ Resume skills: {data['resume_info']['skills']}")
print(f"✓ Top job: {data['matched_jobs'][0]['title']} at {data['matched_jobs'][0]['company']}")
print(f"✓ Top match score: {data['matched_jobs'][0]['match_score']}")

assert data['total_matches'] > 0
print("\n✅ JSON validation passed!")
EOF
```

---

## Level 4: Manual Testing 🧑‍💻

**Time:** 10-15 minutes | **Interactive testing**

### Test 1: Different Resume Profiles

**Test with Junior Developer:**
```bash
echo "Junior Python Developer, 1 year experience, Python, HTML/CSS, New York, NY" > junior.txt
python impl.py --resume junior.txt
# Should find junior-level roles
```

**Test with Senior Manager:**
```bash
echo "Senior Engineering Manager, 10 years experience, Leadership, Team Management, Remote" > manager.txt
python impl.py --resume manager.txt
# Should find management roles
```

**Test with Data Scientist:**
```bash
echo "Data Scientist, Machine Learning, Python, TensorFlow, Pandas, San Francisco, CA" > data_sci.txt
python impl.py --resume data_sci.txt
# Should find ML/DS roles
```

### Test 2: Edge Cases

**Remote Only:**
```bash
python impl.py --resume resume.pdf
# Check if "Remote" jobs appear highly ranked
```

**Location Mismatch:**
```bash
# Resume with Austin, TX; should still find remote positions
```

**Few Skills:**
```bash
# Resume with minimal skills; should still match on title
```

### Test 3: Output Formats

**Terminal Output:**
```bash
python impl.py --resume resume.pdf
# Check colored output, score bars, formatting
```

**JSON Export:**
```bash
python impl.py --resume resume.pdf --output results.json
cat results.json | python -m json.tool
# Verify JSON structure
```

**HTML Export:**
```bash
python3 << 'EOF'
from impl import run_job_finder
from formatter import format_html_results

result = run_job_finder("resume.pdf")
html = format_html_results(result["matched_jobs"])

with open("results.html", "w") as f:
    f.write(html)

print("✓ HTML saved to results.html")
EOF

# Open in browser:
open results.html
```

---

## Level 5: OpenClaw Skill Testing 🤖

**Time:** 5-10 minutes | **Chat interface**

### Step 1: Set Up OpenClaw

```bash
# Copy to OpenClaw skills directory
cp -r /Users/sankar/projects/job_finder ~/.openclaw/skills/job_finder/

# Reload OpenClaw (restart or reload skills)
```

### Step 2: Trigger in Chat

In OpenClaw chat, try:

**Basic Trigger:**
```
"Find me jobs"
[Upload resume.pdf]
```

**Variations:**
```
"job search"
"Find jobs matching my resume"
"match my resume"
"search for jobs"
```

### Step 3: Verify Response

Look for:
- ✓ Resume parsed correctly
- ✓ Job counts from each source
- ✓ Top 10 jobs listed with scores
- ✓ Company summaries (if YOU_API_KEY set)
- ✓ Apply links included

---

## Performance Testing ⚡

### Measure Execution Time
```bash
time python impl.py --resume resume.pdf
```

**Expected Times:**
```
Resume Parse: 0.5-1 sec
Job Scraping: 30-60 sec  (parallel)
Matching: 1-2 sec
Enrichment: 5-10 sec
Total: 40-75 sec
```

### Monitor API Usage
```bash
# Check Apify usage
open https://console.apify.com/usage

# Check You.com usage
open https://you.com/apis
```

---

## Error Testing 🐛

### Test 1: Missing Resume
```bash
python impl.py --resume nonexistent.pdf
# Should show: "❌ Error: Failed to parse resume"
```

### Test 2: Invalid PDF
```bash
echo "This is text, not a PDF" > fake.pdf
python impl.py --resume fake.pdf
# Should handle gracefully
```

### Test 3: Network Issues
```bash
# Disconnect internet, then run:
python impl.py --resume resume.pdf
# Should show: "⚠️ LinkedIn failed: ..."
# But continue with other sources
```

### Test 4: Invalid API Key
```bash
# Edit .env, set APIFY_TOKEN=invalid_key
python impl.py --resume resume.pdf
# Should show clear error message
```

---

## Automated Test Suite 🤖

Create `tests.py`:

```python
#!/usr/bin/env python3
"""Automated test suite for Job Finder Agent."""

import unittest
from pdf_parser import extract_skills, extract_job_title
from matcher import score_job_match, deduplicate_jobs
from formatter import format_single_job


class TestPdfParser(unittest.TestCase):
    def test_skill_extraction(self):
        text = "Python, AWS, Docker"
        skills = extract_skills(text)
        self.assertIn("Python", skills)

    def test_title_extraction(self):
        text = "Senior Python Engineer"
        title = extract_job_title(text)
        self.assertIn("Engineer", title)


class TestMatcher(unittest.TestCase):
    def test_job_scoring(self):
        resume = {
            "title": "Python Engineer",
            "skills": ["Python", "AWS"],
            "location": "SF, CA",
            "level": "senior"
        }
        job = {
            "title": "Senior Python Engineer",
            "description": "Python, AWS required",
            "location": "SF, CA",
            "company": "Google"
        }
        score = score_job_match(job, resume)
        self.assertGreater(score, 0.5)

    def test_deduplication(self):
        jobs = [
            {"title": "Dev", "company": "A"},
            {"title": "Dev", "company": "A"},
            {"title": "Dev", "company": "B"}
        ]
        unique = deduplicate_jobs(jobs)
        self.assertEqual(len(unique), 2)


if __name__ == "__main__":
    unittest.main()
```

Run tests:
```bash
python -m pytest tests.py -v
```

---

## Testing Checklist

- [ ] Setup verification passes
- [ ] Unit tests for parser
- [ ] Unit tests for matcher
- [ ] Unit tests for formatter
- [ ] End-to-end test with sample resume
- [ ] JSON export valid
- [ ] Multiple resume types tested
- [ ] Edge cases handled
- [ ] Error handling works
- [ ] Performance acceptable (< 75 sec)
- [ ] OpenClaw skill integration works
- [ ] All API keys configured
- [ ] Documentation accurate

---

## Quick Test Commands

```bash
# 1. Verify setup (30 sec)
python check.py

# 2. Unit tests (2 min)
python3 << 'EOF'
from pdf_parser import extract_skills
text = "Python, AWS, Docker"
skills = extract_skills(text)
assert len(skills) > 0
print("✓ Parser works")
EOF

# 3. Full integration test (45 sec - 1 min 15 sec)
python impl.py --resume resume.pdf

# 4. Verify JSON output
python3 -c "import json; json.load(open('job_matches.json')); print('✓ JSON valid')"
```

---

**Total Test Time: 1-2 minutes for full test suite** ✅

---

**Status:** Ready to test! 🚀
