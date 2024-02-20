from just_chat.application.common.session_gateway import SessionToken
from just_chat.domain.models.user import User


def test_create_user(client, user_gateway):
    response = client.post(
        r"/user",
        json={
            "username": "Username",
            "password": "123",
        }
    )
    assert response.status_code == 200
    response_json = response.json()

    assert isinstance(response_json["id"], int)
    assert response_json["username"] == "Username"

    user = user_gateway.get_user_by_id(response_json["id"])

    assert user.username == response_json["username"]


def test_get_user_by_id(client, user_gateway):
    user = user_gateway.save_user(User(
        id=None,
        username="Username",
        hashed_password="123"
    ))

    response = client.get(rf"/user/{user.id}")
    assert response.status_code == 200
    response_json = response.json()

    assert response_json["id"] == user.id
    assert response_json["username"] == user.username


def test_login(client, user_gateway, password_provider, session_gateway):
    user = user_gateway.save_user(User(
        id=None,
        username="test_login",
        hashed_password=password_provider.hash_password("123")
    ))

    response = client.post(
        rf"/user/login",
        json={
            "username": user.username,
            "password": "123",
        }
    )

    assert response.status_code == 200
    assert "token" in response.cookies

    session_token = response.cookies.get("token").strip('"')

    session_user_id = session_gateway.get_user_id(SessionToken(session_token))
    assert user.id == session_user_id
