# 🚀 Job Finder Agent - Setup Guide

## Quick Setup (3 Steps)

### 1️⃣ Create Virtual Environment
```bash
cd /Users/sankar/projects/job_finder
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure API Keys
Edit `.env` and add your You.com API key:
```bash
APIFY_TOKEN=apify_api_your_token_here
YOU_API_KEY=your_you_api_key_here  # Get from https://you.com/apis
```

---

## Detailed Setup Steps

### Step 1: Create Virtual Environment

On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **pdfplumber** - PDF resume parsing
- **apify-client** - Apify API wrapper
- **requests** - HTTP library
- **python-dotenv** - Environment variable loading

### Step 3: Verify Setup

Run the verification script:
```bash
python check.py
```

Should show all ✓ checks passing.

### Step 4: Test the Application

Get a sample PDF resume or create one, then run:

```bash
python impl.py --resume path/to/your/resume.pdf
```

**Expected output:**
```
🔍 Job Finder Agent Starting...

📄 Parsing resume...
  ✓ Extracted profile:
    - Title: Python Engineer
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
============================================================

Profile:
  • Title: Python Engineer
  • Level: Senior
  • Location: San Francisco, CA
  • Skills: Python, AWS, Machine Learning, Docker +4 more

Results:
  • Total matches found: 18
  • Average match score: 75%
  • Sources: Linkedin: 12, Indeed: 5, Hackernews: 1

============================================================

🎯 Found 18 matching jobs (showing top 10):

1. Senior Python Engineer at Google
📍 San Francisco, CA | [██████████] 92% match
📌 Source: LinkedIn
💰 Salary: $180K - $250K

Build ML systems at scale. We're looking for experienced Python
engineers with ML background...

🏢 Company: Google is a multinational technology company...

🔗 Apply: https://linkedin.com/jobs/view/...

────────────────────────────────────────────────────────

[... more jobs ...]

💾 Results saved to job_matches.json
```

---

## API Key Setup

### Apify Token (Required)

Already configured in your `.env`:
```
APIFY_TOKEN=apify_api_your_token_here
```

**Note:** This key is now in your `.env` file which is in `.gitignore` (not committed to git).

**⚠️ IMPORTANT:** If you share this repo or push to GitHub, make sure `.gitignore` includes `.env` to prevent accidentally committing API keys.

### You.com API Key (Optional)

1. Go to https://you.com/apis
2. Sign up / Log in
3. Create an API key
4. Add to `.env`:
   ```bash
   YOU_API_KEY=ydc_your_api_key_here
   ```

Without this key, the app still works but skips company enrichment.

---

## Usage

### Command Line

```bash
python impl.py --resume path/to/resume.pdf
```

**Options:**
```bash
python impl.py --resume resume.pdf --output results.json
```

### Python API

```python
from impl import run_job_finder

result = run_job_finder("resume.pdf")

print(result["summary"])           # Print summary
print(result["results"])           # Print formatted jobs
print(result["total_matches"])     # Get count
print(result["matched_jobs"][0])   # Get first job details
```

### As OpenClaw Skill

1. Copy to OpenClaw skills directory:
   ```bash
   cp -r . ~/.openclaw/skills/job_finder/
   ```

2. Reload OpenClaw

3. Use in chat:
   ```
   "Find me jobs matching my resume"
   [Upload resume.pdf]
   ```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'pdfplumber'"
→ Make sure your virtual environment is activated:
```bash
source venv/bin/activate
```

### "APIFY_TOKEN not set"
→ Check `.env` exists and is in the same directory as `impl.py`

### "Failed to parse PDF"
→ Make sure PDF is text-based (not a scanned image)

### No jobs found / low match scores
→ Try with a clearer resume or more specific job title

### Slow execution
→ First run is slower (API initialization). Subsequent runs are faster.

---

## Project Structure

```
job_finder/
├── impl.py                    # Main orchestrator
├── pdf_parser.py              # Resume parsing
├── matcher.py                 # Job ranking algorithm
├── enricher.py                # You.com integration
├── formatter.py               # Output formatting
├── config.py                  # Configuration
├── check.py                   # Setup verification
├── scrapers/
│   ├── apify_client.py        # Apify API wrapper
│   ├── linkedin.py            # LinkedIn scraper
│   ├── indeed.py              # Indeed scraper
│   └── hackernews.py          # HackerNews scraper
├── .env                       # Environment config (in .gitignore)
├── .env.example               # Example config
├── requirements.txt           # Python dependencies
├── README.md                  # Full documentation
├── SKILL.md                   # OpenClaw skill definition
└── SETUP.md                   # This file
```

---

## Performance

| Metric | Time |
|--------|------|
| Resume Parse | 0.5-1 sec |
| Job Scraping | 30-60 sec |
| Matching & Ranking | 1-2 sec |
| Company Enrichment | 5-10 sec |
| **Total** | **40-75 sec** |

---

## Support

- **Apify Docs:** https://docs.apify.com
- **You.com API:** https://you.com/apis
- **pdfplumber:** https://github.com/jsvine/pdfplumber

---

**Ready to find your perfect job!** 🚀
