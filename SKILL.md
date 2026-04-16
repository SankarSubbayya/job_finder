---
name: job-finder
type: skill
description: Find your perfect job by uploading a resume. Searches LinkedIn, Indeed, and HackerNews for matching roles based on your skills and preferences
version: 1.0.0
author: Job Finder Team
tags: [jobs, career, recruitment, resume, employment]
tools:
  - file_read
  - http_request
triggers:
  - "find me jobs"
  - "job search"
  - "match my resume"
  - "find jobs matching my resume"
  - "search for jobs"
author_notes: "Upload your PDF resume and I'll search multiple job boards for positions that match your skills, experience level, and location preferences."
---

# Job Finder Skill

Find your perfect job match in seconds! Upload your PDF resume and I'll search LinkedIn, Indeed, and HackerNews for positions that match your skills and preferences.

## What I Do

1. **Parse Your Resume** - Extract your job title, skills, location, and experience level
2. **Search Multiple Sources** - Search LinkedIn Jobs, Indeed, and HackerNews "Who is Hiring?" threads simultaneously
3. **Smart Matching** - Use AI-powered keyword matching to find jobs that fit your profile (not just keyword dumps!)
4. **Rank Results** - Show you the best matches first, with match scores
5. **Company Research** - Enrich top matches with company information

## How to Use

Simply upload your resume PDF and I'll handle the rest:

```
"Find me jobs matching my resume"
[Upload resume.pdf]
```

## What You'll Get

- **Ranked job listings** sorted by relevance to your profile
- **Match scores** showing how well each job fits
- **Company summaries** for top matches
- **Direct links** to apply
- **JSON export** of all matches

## Features

✅ Multi-source search (LinkedIn, Indeed, HackerNews)
✅ Intelligent keyword matching
✅ Location-aware filtering
✅ Skill-based ranking
✅ Company enrichment with AI research
✅ JSON export for further analysis
✅ Handles remote, hybrid, and on-site roles

## Requirements

- PDF resume (supports most formats)
- Clear job title and skills listed in resume
- Optional: location preferences

## Tips for Best Results

- Use clear, specific job titles
- List all relevant technical and soft skills
- Include your location or indicate if you're open to remote
- Make sure your PDF is readable (not scanned images)

## Sources

- **LinkedIn Jobs**: Real-time job postings from LinkedIn
- **Indeed**: Comprehensive job search engine
- **HackerNews**: Monthly "Who is Hiring?" threads (great for tech roles)

## Privacy

Your resume is processed locally and not stored. Search results are fetched real-time and not cached long-term.

---

**Have questions?** This skill is powered by Apify web scraping and you.com search APIs for real-time job matching.
