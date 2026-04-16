"""Configuration for Job Finder Agent."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
APIFY_TOKEN = os.getenv("APIFY_TOKEN", "")
YOU_API_KEY = os.getenv("YOU_API_KEY", "")

# Apify Actor IDs
LINKEDIN_ACTOR_ID = "bebity/linkedin-jobs-scraper"
INDEED_ACTOR_ID = "misceres/indeed-scraper"
HACKERNEWS_ACTOR_ID = "mstepith19/hacker-news-scraper"

# Job scraping parameters
JOBS_PER_SOURCE = 50
MIN_JOB_SCORE = 0.35  # Minimum keyword match threshold (increased from 0.2 to filter junk)

# you.com API endpoint
YOU_COM_SEARCH_URL = "https://api.you.com/search"

# Skill keywords to look for in resumes
COMMON_SKILLS = [
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust",
    "react", "angular", "vue", "nodejs", "express", "django", "flask",
    "aws", "gcp", "azure", "kubernetes", "docker", "postgres", "mysql",
    "sql", "mongodb", "redis", "elasticsearch", "git", "agile", "scrum",
    "machine learning", "ai", "nlp", "deep learning", "tensorflow", "pytorch",
    "data analysis", "analytics", "tableau", "power bi",
    "leadership", "communication", "project management", "devops"
]

# Job level keywords
LEVEL_KEYWORDS = {
    "junior": ["junior", "entry", "grad", "0-2 years", "entry-level"],
    "mid": ["mid", "2-5 years", "experienced"],
    "senior": ["senior", "5-10 years", "principal", "staff", "lead"],
    "executive": ["director", "vp", "executive", "manager", "head of"]
}
