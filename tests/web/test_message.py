from dataclasses import asdict

import pytest

from just_chat.chat.domain.models.chat import Chat
from just_chat.message.domain.models.message import Message
from just_chat.user.domain.models.user import User


@pytest.mark.asyncio
async def test_send_message_with_access(client, chat_gateway, user_gateway, message_gateway, password_provider):
    user1 = await user_gateway.save_user(User(
        id=None,
        username="send_message_with_access",
        hashed_password=password_provider.hash_password("123")
    ))
    user2 = await user_gateway.save_user(User(
        id=None,
        username="Username2",
        hashed_password="123"
    ))
    chat = await chat_gateway.save_chat(Chat(
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

    message = await message_gateway.get_message_by_id(response_json["id"])

    assert message.text == response_json["text"]
    assert message.author_id == response_json["author_id"]
    assert message.owner_id == response_json["owner_id"]


@pytest.mark.asyncio
async def test_send_message_with_no_access(client, chat_gateway, user_gateway, message_gateway, password_provider):
    user = await user_gateway.save_user(User(
        id=None,
        username="send_message_with_no_access",
        hashed_password=password_provider.hash_password("123")
    ))
    chat = await chat_gateway.save_chat(Chat(
        id=None,
        title="Title",
        users_ids=[],
    ))

    response = client.post(
        r"/user/login",
        json={
            "username": user.username,
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

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_chat_messages_with_access(client, chat_gateway, user_gateway, message_gateway, password_provider):
    user1 = await user_gateway.save_user(User(
        id=None,
        username="get_chat_messages_with_access",
        hashed_password=password_provider.hash_password("123")
    ))
    user2 = await user_gateway.save_user(User(
        id=None,
        username="Username2",
        hashed_password="123"
    ))
    chat = await chat_gateway.save_chat(Chat(
        id=None,
        title="Title",
        users_ids=[user1.id, user2.id],
    ))
    messages = []
    for text in ("Text1", "Text2", "Text3"):
        message = await message_gateway.save_message(Message(
            id=None,
            chat_id=chat.id,
            text=text,
            owner_id=user1.id,
            author_id=user1.id,
        ))

        messages.append(message)

    response = client.post(
        r"/user/login",
        json={
            "username": user1.username,
            "password": "123",
        }
    )

    assert response.status_code == 200
    assert "token" in response.cookies

    response = client.get(
        rf"/message/chat/{chat.id}",
    )

    assert response.status_code == 200
    response_json = response.json()

    for message in messages:
        message_dict = asdict(message)
        assert message_dict in response_json

    for message in response_json:
        assert isinstance(message["id"], int)

    messages_ids = {message["id"] for message in response_json}
    assert messages_ids == messages_ids


@pytest.mark.asyncio
async def test_get_chat_messages_with_no_access(client, chat_gateway, user_gateway, message_gateway, password_provider):
    user1 = await user_gateway.save_user(User(
        id=None,
        username="get_chat_messages_with_no_access",
        hashed_password=password_provider.hash_password("123")
    ))
    chat = await chat_gateway.save_chat(Chat(
        id=None,
        title="Title",
        users_ids=[],
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

    response = client.get(
        rf"/message/chat/{chat.id}",
    )

    assert response.status_code == 403
