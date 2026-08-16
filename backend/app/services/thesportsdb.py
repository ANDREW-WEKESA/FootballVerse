import requests

BASE_URL = "https://www.thesportsdb.com/api/v1/json/123"


def search_player(name):
    response = requests.get(
        f"{BASE_URL}/searchplayers.php",
        params={"p": name},
        timeout=15
    )
    response.raise_for_status()
    return response.json()


def get_player(player_id):
    response = requests.get(
        f"{BASE_URL}/lookupplayer.php",
        params={"id": player_id},
        timeout=15
    )
    response.raise_for_status()
    return response.json()


def get_player_stats(player_id):
    response = requests.get(
        f"{BASE_URL}/lookupplayerstats.php",
        params={"id": player_id},
        timeout=15
    )
    response.raise_for_status()
    return response.json()


def get_player_honours(player_id):
    response = requests.get(
        f"{BASE_URL}/lookuphonours.php",
        params={"id": player_id},
        timeout=15
    )
    response.raise_for_status()
    return response.json()
