"""Keyword matching and job ranking logic."""

from typing import List, Dict
import re
from config import MIN_JOB_SCORE


def score_job_match(job: Dict, resume_keywords: Dict) -> float:
    """
    Score how well a job matches the resume keywords.

    Args:
        job: Job dictionary with title, description, company, etc.
        resume_keywords: Dictionary with 'title', 'skills', 'location', 'level'

    Returns:
        Score between 0 and 1, where 1 is a perfect match
    """
    score = 0.0
    weights = {
        "title": 0.3,
        "skills": 0.4,
        "location": 0.2,
        "company": 0.1
    }

    # Title match (30%)
    title_score = _match_title(
        job.get("title", ""),
        resume_keywords.get("title", ""),
        job.get("description", "")
    )
    score += title_score * weights["title"]

    # Skills match (40%) - most important
    skills_score = _match_skills(
        job.get("title", ""),
        job.get("description", ""),
        resume_keywords.get("skills", [])
    )
    score += skills_score * weights["skills"]

    # Location match (20%)
    location_score = _match_location(
        job.get("location", ""),
        resume_keywords.get("location", "")
    )
    score += location_score * weights["location"]

    # Company reputation (10%)
    company_score = _score_company(job.get("company", ""))
    score += company_score * weights["company"]

    return min(score, 1.0)  # Cap at 1.0


def _match_title(job_title: str, resume_title: str, description: str) -> float:
    """Score title similarity."""
    job_title_lower = job_title.lower()
    resume_title_lower = resume_title.lower()
    description_lower = description.lower()

    # Exact match
    if job_title_lower == resume_title_lower:
        return 1.0

    # Extract key words from resume title
    resume_words = set(resume_title_lower.split())

    # Count matching words in job title
    matching_words = sum(1 for word in resume_words if word in job_title_lower)
    title_match = matching_words / len(resume_words) if resume_words else 0

    # Also check description
    desc_match = sum(1 for word in resume_words if word in description_lower) / len(resume_words) if resume_words else 0

    return min(max(title_match, desc_match * 0.5), 1.0)


def _match_skills(job_title: str, description: str, resume_skills: List[str]) -> float:
    """Score how many resume skills appear in the job posting."""
    if not resume_skills:
        return 0.5  # Default score if no skills extracted

    text = (job_title + " " + description).lower()

    matching_skills = 0
    for skill in resume_skills:
        skill_lower = skill.lower()
        # Look for whole word match
        if re.search(rf'\b{re.escape(skill_lower)}\b', text):
            matching_skills += 1

    return min(matching_skills / len(resume_skills), 1.0)


def _match_location(job_location: str, resume_location: str) -> float:
    """Score location match."""
    job_loc_lower = job_location.lower()
    resume_loc_lower = resume_location.lower()

    # Remote job is always acceptable
    if "remote" in job_loc_lower:
        return 0.9

    # Exact match
    if job_loc_lower == resume_loc_lower:
        return 1.0

    # Partial match (city or state)
    job_parts = job_loc_lower.split(",")
    resume_parts = resume_loc_lower.split(",")

    matching_parts = sum(1 for jp in job_parts if any(jp.strip() == rp.strip() for rp in resume_parts))

    if matching_parts > 0:
        return 0.7

    return 0.3  # Different location but not penalized heavily


def _score_company(company_name: str) -> float:
    """Score company desirability (simple heuristic)."""
    if not company_name or company_name == "Unknown":
        return 0.5

    # Well-known tech companies get higher scores
    top_companies = [
        "google", "microsoft", "apple", "amazon", "meta",
        "tesla", "netflix", "stripe", "airbnb", "uber",
        "coinbase", "github", "nvidia", "openai"
    ]

    company_lower = company_name.lower()
    if any(tc in company_lower for tc in top_companies):
        return 1.0

    return 0.7  # Default company score


def rank_jobs(
    jobs: List[Dict],
    resume_keywords: Dict,
    min_score: float = MIN_JOB_SCORE
) -> List[Dict]:
    """
    Rank jobs by match score.

    Args:
        jobs: List of job dictionaries
        resume_keywords: Resume keyword dictionary
        min_score: Minimum score to include (0.2 by default)

    Returns:
        Sorted list of jobs with scores, filtered by min_score
    """
    scored_jobs = []

    for job in jobs:
        score = score_job_match(job, resume_keywords)

        if score >= min_score:
            job_with_score = job.copy()
            job_with_score["match_score"] = round(score, 2)
            scored_jobs.append(job_with_score)

    # Sort by score descending
    scored_jobs.sort(key=lambda x: x["match_score"], reverse=True)

    return scored_jobs


def deduplicate_jobs(jobs: List[Dict]) -> List[Dict]:
    """Remove duplicate jobs from list."""
    seen = set()
    unique_jobs = []

    for job in jobs:
        # Use title + company as unique identifier
        key = (job.get("title", "").lower(), job.get("company", "").lower())

        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    return unique_jobs
