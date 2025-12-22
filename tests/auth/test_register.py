def test_registration(client):
    res = client.post("/api/v1/auth/register/", json={
        "username": "bob",
        "email": "bob@test.com",
        "password": "password123",
        "password_confirm": "password123"
    })
    assert res.status_code == 201
    assert res.json.get("message") == "User registered successfully"
    
    
