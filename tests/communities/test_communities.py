def test_create_community(client, auth_headers):
    client.post("/api/v1/auth/register/", json={
        "username": "tom",
        "email": "mod@test.com",
        "password": "password123",
        "password_confirm": "password123"
    })
    headers = auth_headers("mod@test.com", "password123")
    
    res = client.post("/api/v1/communities/", json={
        "name": "youth-dev",
        "description": "Tech with in youth"
    }, headers=headers)
    
    assert res.status_code == 201