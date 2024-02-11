def test_create_user(client):
    response = client.post(
        r"/user",
        json={
            "username": "Username",
            "password": "123",
        }
    )

    response_json = response.json()

    assert response_json["username"] == "Username"
    assert isinstance(response_json["id"], int)
