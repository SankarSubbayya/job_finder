"""Wrapper for Apify Actor API calls."""

from apify_client import ApifyClient
from typing import List, Dict, Any
from config import APIFY_TOKEN


def run_actor(actor_id: str, run_input: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Run an Apify actor and return results.

    Args:
        actor_id: Apify actor ID (e.g., "bebity/linkedin-jobs-scraper")
        run_input: Input parameters for the actor

    Returns:
        List of results from the actor's dataset
    """
    if not APIFY_TOKEN:
        raise ValueError("APIFY_TOKEN environment variable not set")

    client = ApifyClient(APIFY_TOKEN)

    try:
        # Run the actor
        run = client.actor(actor_id).call(run_input=run_input)

        # Get results from the dataset
        results = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            results.append(item)

        return results

    except Exception as e:
        print(f"Error running actor {actor_id}: {e}")
        return []


def run_actor_with_timeout(
    actor_id: str,
    run_input: Dict[str, Any],
    timeout_secs: int = 300
) -> List[Dict[str, Any]]:
    """
    Run an Apify actor with a timeout.

    Args:
        actor_id: Apify actor ID
        run_input: Input parameters
        timeout_secs: Timeout in seconds

    Returns:
        List of results
    """
    if not APIFY_TOKEN:
        raise ValueError("APIFY_TOKEN environment variable not set")

    client = ApifyClient(APIFY_TOKEN)

    try:
        # Run the actor with timeout
        run = client.actor(actor_id).call(
            run_input=run_input,
            timeout_secs=timeout_secs
        )

        # Get results from the dataset
        results = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            results.append(item)

        return results

    except Exception as e:
        print(f"Error running actor {actor_id}: {e}")
        return []
