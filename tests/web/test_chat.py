from just_chat.domain.models.chat import Chat
from just_chat.domain.models.user import User


def test_create_chat(client, chat_gateway, user_gateway):
    user1 = user_gateway.save_user(User(
        id=None,
        username="Username1",
        hashed_password="123"
    ))
    user2 = user_gateway.save_user(User(
        id=None,
        username="Username2",
        hashed_password="123"
    ))

    response = client.post(
        r"/chat",
        json={
            "title": "Title",
            "user_ids": [user1.id, user2.id],
        }
    )
    assert response.status_code == 200
    response_json = response.json()

    assert isinstance(response_json["id"], int)
    assert response_json["users_ids"] == [user1.id, user2.id]
    assert response_json["title"] == "Title"

    chat = chat_gateway.get_chat_by_id(response_json["id"])

    assert chat.title == response_json["title"]
    assert chat.users_ids == response_json["users_ids"]


def test_create_chat_with_random_user(
        client,
        chat_gateway,
        user_gateway,
        password_provider
):
    user1 = user_gateway.save_user(User(
        id=None,
        username="username13",
        hashed_password=password_provider.hash_password("123")
    ))
    user2 = user_gateway.save_user(User(
        id=None,
        username="Username2",
        hashed_password=password_provider.hash_password("123")
    ))

    response = client.post(
        r"/user/login",
        json={
            "username": "username13",
            "password": "123"
        }
    )

    assert response.status_code == 200
    assert "token" in response.cookies

    response = client.post(
        r"/chat/random",
        json={
            "title": "Title",
        }
    )

    assert response.status_code == 200

    response_json = response.json()

    assert isinstance(response_json["id"], int)
    assert len(response_json["users_ids"]) == 2
    assert response_json["title"] == "Title"

    chat = chat_gateway.get_chat_by_id(response_json["id"])

    assert chat.title == response_json["title"]
    assert chat.users_ids == response_json["users_ids"]


def test_get_chat_by_id(client, chat_gateway, user_gateway):
    user1 = user_gateway.save_user(User(
        id=None,
        username="Username1",
        hashed_password="123"
    ))
    user2 = user_gateway.save_user(User(
        id=None,
        username="Username2",
        hashed_password="123"
    ))
    chat = chat_gateway.save_chat(Chat(
        id=None,
        title="Title",
        users_ids=[user1.id, user2.id],
    ))

    response = client.get(rf"/chat/{chat.id}")
    assert response.status_code == 200
    response_json = response.json()

    assert response_json["id"] == chat.id
    assert response_json["users_ids"] == [user1.id, user2.id]
    assert response_json["title"] == "Title"


def test_delete_chat_by_id(client, chat_gateway, user_gateway):
    user1 = user_gateway.save_user(User(
        id=None,
        username="Username1",
        hashed_password="123"
    ))
    user2 = user_gateway.save_user(User(
        id=None,
        username="Username2",
        hashed_password="123"
    ))
    chat = chat_gateway.save_chat(Chat(
        id=None,
        title="Title",
        users_ids=[user1.id, user2.id],
    ))

    response = client.delete(rf"/chat/{chat.id}")
    assert response.status_code == 200
    response_json = response.json()

    assert response_json["id"] == chat.id
    assert response_json["users_ids"] == [user1.id, user2.id]
    assert response_json["title"] == "Title"
