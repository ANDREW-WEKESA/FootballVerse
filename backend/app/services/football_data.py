import os
import requests
from datetime import datetime

FOOTBALL_DATA_URL = "https://api.football-data.org/v4"


def get_headers():
    token = os.getenv("FOOTBALL_DATA_API_KEY")
    if not token:
        raise RuntimeError("FOOTBALL_DATA_API_KEY is not configured")
    return {"X-Auth-Token": token}


def fetch_competitions():
    response = requests.get(
        f"{FOOTBALL_DATA_URL}/competitions",
        headers=get_headers(),
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def fetch_team(team_id):
    response = requests.get(
        f"{FOOTBALL_DATA_URL}/teams/{team_id}",
        headers=get_headers(),
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def fetch_player(player_id):
    response = requests.get(
        f"{FOOTBALL_DATA_URL}/persons/{player_id}",
        headers=get_headers(),
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def sync_status():
    return {
        "service": "FootballVerse Data Sync",
        "provider": "football-data.org",
        "status": "ready",
        "last_sync": datetime.utcnow().isoformat()
    }
