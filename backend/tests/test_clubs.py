def test_create_and_list_club(client, admin_headers):
    resp = client.post(
        "/clubs",
        json={"name": "Riverside United", "country": "Wales"},
        headers=admin_headers,
    )
    assert resp.status_code == 201
    club = resp.json()
    assert club["name"] == "Riverside United"

    resp = client.get("/clubs")
    assert resp.status_code == 200
    names = [c["name"] for c in resp.json()]
    assert "Riverside United" in names


def test_get_club_not_found(client):
    resp = client.get("/clubs/999999")
    assert resp.status_code == 404


def test_update_club(client, admin_headers):
    create = client.post(
        "/clubs",
        json={"name": "Old Name FC", "country": "Scotland"},
        headers=admin_headers,
    )
    club_id = create.json()["id"]

    resp = client.put(
        f"/clubs/{club_id}",
        json={"name": "New Name FC"},
        headers=admin_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "New Name FC"


def test_delete_club(client, admin_headers):
    create = client.post(
        "/clubs",
        json={"name": "Temporary FC", "country": "Ireland"},
        headers=admin_headers,
    )
    club_id = create.json()["id"]

    resp = client.delete(f"/clubs/{club_id}", headers=admin_headers)
    assert resp.status_code == 200

    resp = client.get(f"/clubs/{club_id}")
    assert resp.status_code == 404


def test_story_requires_player_or_club(client, admin_headers):
    resp = client.post(
        "/stories",
        json={"title": "A story with no subject"},
        headers=admin_headers,
    )
    assert resp.status_code == 422


def test_story_creation_with_club(client, admin_headers):
    club = client.post(
        "/clubs",
        json={"name": "Story Club FC", "country": "France"},
        headers=admin_headers,
    ).json()

    resp = client.post(
        "/stories",
        json={"title": "The rise of Story Club FC", "club_id": club["id"]},
        headers=admin_headers,
    )
    assert resp.status_code == 201
    assert resp.json()["club_id"] == club["id"]
