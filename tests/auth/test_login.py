def test_loginnow(client):
    client.post("/api/v1/auth/register/", json={
        "username": "alice",
        "email": "alice@test.com",
        "password": "password123",
        "password_confirm": "password123"
    })
    res = client.post("/api/v1/auth/login/", json={
        "email": "alice@test.com",
        "password": "password123"
    })
    assert res.status_code == 200
    assert "tokens" in res.json
    assert "access" in res.json["tokens"]
    assert "refresh" in res.json["tokens"]