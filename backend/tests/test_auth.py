import os


def test_health_check(client):
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "running"


def test_login_success(client):
    resp = client.post(
        "/auth/login",
        json={
            "email": os.environ["ADMIN_EMAIL"],
            "password": os.environ["ADMIN_PASSWORD"],
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_wrong_password(client):
    resp = client.post(
        "/auth/login",
        json={"email": os.environ["ADMIN_EMAIL"], "password": "wrong-password"},
    )
    assert resp.status_code == 401


def test_login_unknown_user(client):
    resp = client.post(
        "/auth/login",
        json={"email": "nobody@example.com", "password": "whatever"},
    )
    assert resp.status_code == 401


def test_admin_only_endpoint_requires_auth(client):
    resp = client.post("/clubs", json={"name": "Test FC", "country": "England"})
    assert resp.status_code in (401, 403)


def test_admin_only_endpoint_with_token(client, admin_headers):
    resp = client.post(
        "/clubs",
        json={"name": "Auth Test FC", "country": "England"},
        headers=admin_headers,
    )
    assert resp.status_code == 201
