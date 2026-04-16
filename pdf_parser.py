"""Parse PDF resume and extract job-relevant keywords."""

import re
import pdfplumber
from typing import Dict, List
from config import COMMON_SKILLS, LEVEL_KEYWORDS


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from PDF file."""
    text = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text.append(page.extract_text())
        return "\n".join(text)
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {e}")


def extract_skills(text: str) -> List[str]:
    """Extract technical skills from resume text."""
    text_lower = text.lower()
    found_skills = []

    for skill in COMMON_SKILLS:
        # Use word boundaries to avoid partial matches
        if re.search(rf'\b{re.escape(skill)}\b', text_lower):
            found_skills.append(skill.title())

    return list(set(found_skills))  # Remove duplicates


def extract_job_title(text: str) -> str:
    """Extract current/last job title from resume."""
    text_lower = text.lower()

    # Look for common job title patterns
    title_patterns = [
        r'(?:current\s+)?(?:title|position|role):\s*([^\n]+)',
        r'(?:senior|junior|lead|principal|staff|director)?\s*(\w+(?:\s+\w+)*)\s*(?:engineer|developer|analyst|manager|architect)',
    ]

    for pattern in title_patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            if title and len(title) > 3:
                return title.title()

    return "Software Engineer"  # Default fallback


def extract_location(text: str) -> str:
    """Extract location/city from resume."""
    # Look for city, state patterns (e.g., "San Francisco, CA")
    pattern = r'([A-Z][a-z]+),\s*([A-Z]{2})|([A-Z][a-z]+),\s*([A-Z][a-z]{1,})'
    match = re.search(pattern, text)

    if match:
        city = match.group(1) or match.group(3)
        state = match.group(2) or match.group(4)
        return f"{city}, {state}"

    # Fallback: try to find "Based in" pattern
    pattern = r'(?:based|located)?\s+(?:in|@)\s+([^,\n]+)'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    return "Remote"  # Default fallback


def extract_experience_level(text: str) -> str:
    """Determine experience level from resume."""
    text_lower = text.lower()

    # Look for years of experience
    years_match = re.search(r'(\d+)\s*(?:\+)?\s*years?', text_lower)
    if years_match:
        years = int(years_match.group(1))
        if years < 2:
            return "junior"
        elif years < 5:
            return "mid"
        elif years < 10:
            return "senior"
        else:
            return "executive"

    # Check for level keywords
    for level, keywords in LEVEL_KEYWORDS.items():
        for keyword in keywords:
            if re.search(rf'\b{re.escape(keyword)}\b', text_lower):
                return level

    return "mid"  # Default to mid-level


def parse_resume(pdf_path: str) -> Dict[str, any]:
    """
    Parse resume PDF and extract structured information.

    Returns:
        {
            "title": str,           # Job title
            "skills": [str],        # List of technical skills
            "location": str,        # Location
            "level": str,          # Experience level (junior/mid/senior/executive)
            "raw_text": str        # Full extracted text
        }
    """
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)

    # Extract structured info
    return {
        "title": extract_job_title(text),
        "skills": extract_skills(text),
        "location": extract_location(text),
        "level": extract_experience_level(text),
        "raw_text": text
    }


if __name__ == "__main__":
    # Test script
    import sys
    if len(sys.argv) < 2:
        print("Usage: python pdf_parser.py <resume.pdf>")
        sys.exit(1)

    result = parse_resume(sys.argv[1])
    print(f"Job Title: {result['title']}")
    print(f"Skills: {', '.join(result['skills'])}")
    print(f"Location: {result['location']}")
    print(f"Level: {result['level']}")
