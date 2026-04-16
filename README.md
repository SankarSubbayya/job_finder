# 🎯 Job Finder Agent

> **An intelligent AI-powered job matching system that analyzes your resume and searches multiple job boards in real-time to find positions perfectly aligned with your skills and experience.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/status-active-brightgreen.svg)](https://github.com)

---

## 📖 Table of Contents

- [Features](#-features)
- [Project Description](#-project-description)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
  - [Web UI](#web-ui)
  - [Command Line](#command-line)
  - [Python API](#python-api)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🔍 Multi-Source Job Search
- **LinkedIn Jobs** - Real-time job postings via Apify
- **Indeed** - Comprehensive job listings
- **HackerNews** - Monthly "Who is Hiring?" threads for startup roles

### 🧠 Intelligent Resume Parsing
- Extract job title, skills, location, and experience level
- Support for various resume formats
- Automatic skill detection from text

### ⭐ Smart Job Matching
- **Weighted Scoring Algorithm:**
  - 40% Skills match (most important)
  - 30% Job title relevance
  - 20% Location compatibility
  - 10% Company reputation
- Deduplication across sources
- Configurable match thresholds

### 🏢 Company Enrichment
- Real-time company research via You.com API
- Company summaries and descriptions
- Benefits and perks information
- Enhanced job decision-making

### 📊 Multiple Output Formats
- **Terminal** - Colored, human-readable output with progress bars
- **JSON** - Structured data for further processing
- **HTML** - Web-viewable format (optional)

### 🎨 Beautiful Web UI
- Claude-style modern interface
- Drag-and-drop resume upload
- Real-time progress tracking
- Color-coded match scores
- Direct apply links
- Responsive design (desktop, tablet, mobile)

### ⚡ Fast & Reliable
- Parallel job scraping (30-60 seconds for 150+ jobs)
- Comprehensive error handling
- Graceful fallbacks if sources fail
- Timeout management

---

## 💡 Project Description

### The Problem
Job searching is time-consuming and inefficient. Most job boards rely on simple keyword matching, showing irrelevant results. Users waste hours sorting through positions that don't match their skills or career goals.

### The Solution
**Job Finder Agent** automates intelligent job matching by:

1. **Parsing Your Resume** - Extracts structured job profile data
2. **Searching Multiple Sources** - Finds jobs across LinkedIn, Indeed, and HackerNews simultaneously
3. **Intelligent Matching** - Uses weighted scoring to rank jobs by relevance, not just keywords
4. **Enriching Results** - Adds company research and details for informed decisions
5. **Beautiful Presentation** - Shows results in easy-to-understand format (web or CLI)

### Why It's Different

| Feature | Job Finder | Generic Job Board |
|---------|-----------|------------------|
| **Matching Algorithm** | Weighted multi-factor | Simple keyword search |
| **Company Research** | AI-powered (You.com) | Manual lookup needed |
| **Multiple Sources** | 3 platforms unified | Single platform |
| **Resume Analysis** | Automatic extraction | Manual profile creation |
| **Match Scoring** | Relevance-based (0-100%) | No scoring |
| **User Experience** | Beautiful UI | Basic interface |

### Use Cases

- 🔄 **Career Changers** - Find roles matching your transferable skills
- 🚀 **Job Seekers** - Discover perfect matches faster
- 🎓 **Graduates** - Find entry-level positions matching your skills
- 📈 **Promotions** - Identify senior/management roles
- 🌍 **Remote Workers** - Filter remote-friendly positions
- 🤖 **Automation** - Integrate into job hunting workflows

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- UV package manager (or pip)
- Apify account (free tier available)
- You.com API key (optional, for company enrichment)

### Installation (5 minutes)

```bash
# 1. Clone/navigate to project
cd /Users/sankar/projects/job_finder

# 2. Create virtual environment
uv venv
source .venv/bin/activate

# 3. Install dependencies
uv sync

# 4. Verify setup
python check.py

# Should show: ✅ All checks passed!
```

### Configuration

1. **Get API Keys:**
   - Apify: https://console.apify.com/account/integrations
   - You.com: https://you.com/apis (optional)

2. **Add to `.env`:**
   ```bash
   APIFY_TOKEN=your_apify_token_here
   YOU_API_KEY=your_you_api_key_here
   ```

3. **Test:**
   ```bash
   python check.py
   ```

---

## 📖 Usage

### 🌐 Web UI (Recommended)

```bash
# Start web server
python app.py

# Open browser
open http://localhost:5000
```

**Features:**
- Clean, Claude-style interface
- Drag-and-drop resume upload
- Real-time progress updates
- Beautiful job cards
- Export results as JSON

See [WEB_SETUP.md](WEB_SETUP.md) for detailed web UI guide.

### 💻 Command Line

```bash
# Basic usage
python impl.py --resume path/to/resume.pdf

# With custom output
python impl.py --resume resume.pdf --output results.json

# Example output:
# 🔍 Job Finder Agent Starting...
# 📄 Parsing resume... ✓
# 🕷️  Scraping job boards... ✓
# ⭐ Ranking jobs... ✓ 18 matches
# 🏢 Enriching with company info... ✓
# ✨ Formatting results...
# ✅ Job Finder Complete!
#
# 📋 Your Job Search Summary
# [... 10 top jobs with details ...]
# 💾 Results saved to job_matches.json
```

### 🐍 Python API

```python
from impl import run_job_finder

# Run job finder
result = run_job_finder("resume.pdf")

# Access results
print(f"Found {result['total_matches']} matching jobs")
print(f"Top match: {result['matched_jobs'][0]['title']}")

# Work with data
for job in result['matched_jobs']:
    print(f"{job['title']} at {job['company']}: {job['match_score']*100:.0f}% match")
```

---

## 🏗️ Architecture

### System Flow

```
Resume (PDF)
    ↓
┌─────────────────────────┐
│  PDF Parser             │  Extract text, skills, title, location, level
└─────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│  Parallel Job Scraping                          │
├─────────────────────────────────────────────────┤
│ LinkedIn Jobs │ Indeed Jobs │ HackerNews Jobs  │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────┐
│  Deduplication          │  Remove duplicate jobs across sources
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│  Job Matching           │  Score each job (0-1 scale)
│  & Ranking              │  - Skills match (40%)
│                         │  - Title match (30%)
│                         │  - Location (20%)
│                         │  - Company (10%)
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│  Company Enrichment     │  Add company info via You.com API
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│  Formatting             │  Terminal, JSON, or HTML output
└─────────────────────────┘
    ↓
Results (Ranked Jobs with Details)
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Resume Parsing** | pdfplumber | Extract text from PDFs |
| **Job Scraping** | Apify API | Access LinkedIn, Indeed, HackerNews |
| **Company Research** | You.com API | Enrich results with company info |
| **Matching Algorithm** | Python | Weighted scoring system |
| **Web Framework** | Flask | Web server and API |
| **Frontend** | HTML/CSS/JS | Beautiful user interface |
| **Package Manager** | UV | Fast Python dependency management |

---

## 📁 Project Structure

```
job_finder/
├── Core Implementation
│   ├── impl.py                 # Main orchestrator (156 lines)
│   ├── pdf_parser.py           # Resume parsing (138 lines)
│   ├── matcher.py              # Job ranking algorithm (187 lines)
│   ├── enricher.py             # You.com integration (136 lines)
│   ├── formatter.py            # Output formatting (145 lines)
│   └── config.py               # Configuration (42 lines)
│
├── Job Scrapers
│   ├── scrapers/
│   │   ├── apify_client.py     # Apify API wrapper (78 lines)
│   │   ├── linkedin.py         # LinkedIn scraper (60 lines)
│   │   ├── indeed.py           # Indeed scraper (60 lines)
│   │   └── hackernews.py       # HackerNews scraper (126 lines)
│
├── Web Application
│   ├── app.py                  # Flask server
│   ├── templates/
│   │   └── index.html          # Main HTML page
│   └── static/
│       ├── css/style.css       # Claude-style CSS
│       └── js/app.js           # Frontend JavaScript
│
├── Configuration
│   ├── pyproject.toml          # Python project config
│   ├── requirements.txt        # Dependencies
│   ├── .env.example            # Config template
│   └── .gitignore              # Git exclusions
│
├── Documentation
│   ├── README.md               # This file
│   ├── SETUP.md                # Detailed setup guide
│   ├── UV_SETUP.md             # UV package manager guide
│   ├── WEB_SETUP.md            # Web UI guide
│   ├── TESTING.md              # Testing guide
│   ├── SUBMISSION.md           # Hackathon submission
│   └── COMPLETION.md           # Project completion
│
├── Utilities
│   ├── check.py                # Setup verification script
│   └── uploads/                # Temporary resume storage
│
└── Total: ~1,200 lines of production Python code
```

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Required: Apify API Token
# Get from: https://console.apify.com/account/integrations
APIFY_TOKEN=your_apify_token_here

# Optional: You.com API Key (for company enrichment)
# Get from: https://you.com/apis
YOU_API_KEY=your_you_api_key_here
```

### Configurable Parameters (config.py)

```python
JOBS_PER_SOURCE = 50           # Max jobs per scraper
MIN_JOB_SCORE = 0.2            # Minimum match threshold (0-1)
COMMON_SKILLS = [...]          # Skills to detect
LEVEL_KEYWORDS = {...}         # Experience level patterns
```

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Resume Parse Time | 0.5-1 sec |
| Job Scraping (parallel) | 30-60 sec |
| Matching & Ranking | 1-2 sec |
| Company Enrichment | 5-10 sec |
| **Total Time** | **40-75 sec** |
| **Jobs Processed** | **150-200** |
| **Top Matches** | **10-20** |

---

## 🧪 Testing

### Quick Verification
```bash
python check.py
```

### Full Integration Test
```bash
python impl.py --resume test_resume.pdf
```

### Web UI Test
```bash
python app.py
# Visit http://localhost:5000
```

See [TESTING.md](TESTING.md) for comprehensive testing guide.

---

## 🔒 Security

- ✅ API keys stored in `.env` (in `.gitignore`, not in version control)
- ✅ No hardcoded secrets
- ✅ PDF parsing sandboxed
- ✅ Request timeouts prevent hanging
- ✅ File upload validation (PDF only, max 16MB)
- ✅ Safe error messages (no key leakage)

**Never commit `.env` to version control!**

---

## 🤝 Contributing

### Development Setup
```bash
uv venv
source .venv/bin/activate
uv sync
```

### Code Style
- Python 3.8+ compatible
- Clear variable names
- Minimal comments (code is self-documenting)
- Error handling for all components

### Adding Features
1. Create feature branch
2. Update relevant module
3. Update tests in [TESTING.md](TESTING.md)
4. Update documentation
5. Commit with clear message

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| [SETUP.md](SETUP.md) | Complete setup instructions |
| [UV_SETUP.md](UV_SETUP.md) | UV package manager guide |
| [WEB_SETUP.md](WEB_SETUP.md) | Web UI detailed guide |
| [TESTING.md](TESTING.md) | Testing and troubleshooting |
| [SUBMISSION.md](SUBMISSION.md) | Hackathon submission details |
| [COMPLETION.md](COMPLETION.md) | Project completion checklist |

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
```bash
uv sync
```

### "APIFY_TOKEN not set"
1. Check `.env` file exists
2. Verify token from https://console.apify.com
3. Make sure `.env` is in project root

### No jobs found
- Ensure resume has clear job title
- Add more technical skills to resume
- Try less specific job titles
- Check internet connection

### Slow execution
- First run initializes APIs
- Subsequent runs are faster
- Apify actors may take 30-60 seconds

See [TESTING.md](TESTING.md) for more troubleshooting.

---

## 📞 Support

- **Apify Docs:** https://docs.apify.com
- **You.com API:** https://you.com/apis
- **pdfplumber:** https://github.com/jsvine/pdfplumber
- **Flask:** https://flask.palletsprojects.com/

---

## 📄 License

MIT License - Free to use and modify

---

## 🎉 Getting Started

```bash
# 1. Setup
cd job_finder
uv venv
source .venv/bin/activate
uv sync

# 2. Configure
# Edit .env with your API keys

# 3. Run (choose one)
python impl.py --resume resume.pdf      # CLI
# OR
python app.py                            # Web UI at localhost:5000

# 4. View results
# CLI: Terminal output + job_matches.json
# Web: Beautiful browser interface
```

---

## 🚀 Next Steps

1. **[Quick Start](#-quick-start)** - Get up and running
2. **[SETUP.md](SETUP.md)** - Detailed setup guide
3. **[WEB_SETUP.md](WEB_SETUP.md)** - Use beautiful web UI
4. **[TESTING.md](TESTING.md)** - Test the application
5. **Find jobs!** - Upload resume and search

---

**Built with ❤️ for the OpenClaw Hackathon 2026**

*Find your perfect job in 45-75 seconds!* 🎯
