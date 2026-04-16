"""Format job search results for display."""

from typing import List, Dict


def format_job_results(jobs: List[Dict], max_results: int = 10) -> str:
    """
    Format jobs for display/return to user.

    Args:
        jobs: List of ranked job dictionaries with match_score
        max_results: Max number of jobs to return

    Returns:
        Formatted string representation
    """
    if not jobs:
        return "No matching jobs found. Try adjusting your location or job title preferences."

    output = f"🎯 Found {len(jobs)} matching jobs (showing top {min(len(jobs), max_results)}):\n\n"

    for i, job in enumerate(jobs[:max_results], 1):
        output += format_single_job(job, i)
        output += "\n" + "—" * 60 + "\n\n"

    return output


def format_single_job(job: Dict, rank: int = None) -> str:
    """Format a single job for display."""
    rank_str = f"{rank}. " if rank else ""
    score = job.get("match_score", 0)
    score_bar = _get_score_bar(score)

    output = f"{rank_str}{job.get('title', 'Position')} at {job.get('company', 'Unknown')}\n"
    output += f"📍 {job.get('location', 'Unknown Location')} | {score_bar} {score * 100:.0f}% match\n"

    if job.get("source"):
        output += f"📌 Source: {job['source'].capitalize()}\n"

    if job.get("salary"):
        output += f"💰 Salary: {job['salary']}\n"

    description = job.get("description", "")
    if description:
        # Truncate long descriptions
        if len(description) > 200:
            description = description[:200] + "..."
        output += f"\n{description}\n"

    if job.get("company_summary"):
        output += f"\n📊 Company: {job['company_summary']}\n"

    if job.get("url"):
        output += f"\n🔗 Apply: {job['url']}\n"

    return output


def format_matching_summary(
    jobs: List[Dict],
    resume_info: Dict
) -> str:
    """Format a summary of the match."""
    output = "📋 Your Job Search Summary\n"
    output += "=" * 60 + "\n\n"

    output += f"Profile:\n"
    output += f"  • Title: {resume_info.get('title', 'Unknown')}\n"
    output += f"  • Level: {resume_info.get('level', 'Unknown').capitalize()}\n"
    output += f"  • Location: {resume_info.get('location', 'Remote')}\n"
    output += f"  • Skills: {', '.join(resume_info.get('skills', [])[:5])}"

    if len(resume_info.get('skills', [])) > 5:
        output += f" +{len(resume_info['skills']) - 5} more"

    output += "\n\n"

    output += f"Results:\n"
    output += f"  • Total matches found: {len(jobs)}\n"

    if jobs:
        avg_score = sum(j.get("match_score", 0) for j in jobs) / len(jobs)
        output += f"  • Average match score: {avg_score * 100:.0f}%\n"

        # Source breakdown
        sources = {}
        for job in jobs:
            source = job.get("source", "unknown")
            sources[source] = sources.get(source, 0) + 1

        output += f"  • Sources: {', '.join(f'{k.capitalize()}: {v}' for k, v in sources.items())}\n"

    output += "\n" + "=" * 60 + "\n"

    return output


def _get_score_bar(score: float, width: int = 10) -> str:
    """Create a visual score bar."""
    filled = int(score * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}]"


def format_html_results(jobs: List[Dict], max_results: int = 10) -> str:
    """Format jobs as HTML for web display."""
    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial; margin: 20px; }
            .job-card {
                border: 1px solid #ddd;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
            }
            .job-title { font-size: 18px; font-weight: bold; }
            .company { color: #666; }
            .score { float: right; color: green; font-weight: bold; }
            .details { margin-top: 10px; font-size: 14px; }
        </style>
    </head>
    <body>
        <h1>Job Matches</h1>
    """

    for i, job in enumerate(jobs[:max_results], 1):
        score_percent = job.get("match_score", 0) * 100
        html += f"""
        <div class="job-card">
            <div class="score">{score_percent:.0f}% match</div>
            <div class="job-title">{job.get('title', 'Position')}</div>
            <div class="company">{job.get('company', 'Unknown')} | {job.get('location', 'Remote')}</div>
            <div class="details">
                <p>{job.get('description', '')[:200]}...</p>
                <a href="{job.get('url', '#')}" target="_blank">View Job →</a>
            </div>
        </div>
        """

    html += "</body></html>"
    return html
