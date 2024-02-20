from just_chat.domain.models.chat import Chat
from just_chat.domain.models.user import User


def test_send_message_with_access(client, chat_gateway, user_gateway, message_gateway, password_provider):
    user1 = user_gateway.save_user(User(
        id=None,
        username="send_message_with_access",
        hashed_password=password_provider.hash_password("123")
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

    response = client.post(
        r"/user/login",
        json={
            "username": user1.username,
            "password": "123",
        }
    )

    assert response.status_code == 200
    assert "token" in response.cookies

    response = client.post(
        r"/message",
        json={
            "chat_id": chat.id,
            "text": "MessageText",
        }
    )

    assert response.status_code == 200
    response_json = response.json()

    assert isinstance(response_json["id"], int)
    assert response_json["text"] == "MessageText"
    assert response_json["author_id"] == user1.id
    assert response_json["owner_id"] == user1.id

    message = message_gateway.get_message_by_id(response_json["id"])

    assert message.text == response_json["text"]
    assert message.author_id == response_json["author_id"]
    assert message.owner_id == response_json["owner_id"]
