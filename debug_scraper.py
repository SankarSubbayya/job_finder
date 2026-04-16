"""Debug script to check what Apify actors actually return."""

from scrapers.apify_client import run_actor_with_timeout
from config import INDEED_ACTOR_ID
import json

print("Testing Indeed scraper to see actual Apify response...")
print("=" * 60)

run_input = {
    "position": "Python Engineer",
    "location": "San Francisco",
    "maxResults": 5
}

try:
    results = run_actor_with_timeout(INDEED_ACTOR_ID, run_input, timeout_secs=120)

    if results:
        print(f"\n✓ Got {len(results)} results from Apify")
        print(f"\nFirst job object keys:")
        first_job = results[0]
        for key in sorted(first_job.keys()):
            value = first_job[key]
            if isinstance(value, str):
                preview = value[:60] + "..." if len(value) > 60 else value
                print(f"  - {key}: '{preview}'")
            else:
                print(f"  - {key}: {type(value).__name__}")

        print(f"\n\nFull first job object:")
        print(json.dumps(first_job, indent=2))
    else:
        print("❌ No results from Apify")

except Exception as e:
    print(f"❌ Error: {e}")
