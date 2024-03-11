import pytest

from just_chat.chat.domain.models.chat import Chat
from just_chat.user.domain.models.user import User


@pytest.mark.asyncio
async def test_new_message_event(
        client,
        chat_gateway,
        user_gateway,
        message_gateway,
        password_provider,
        session_gateway,
        transaction_manager,
):
    user1 = await user_gateway.save_user(User(
        id=None,
        username="new_message_event1",
        hashed_password=password_provider.hash_password("123")
    ))
    user2 = await user_gateway.save_user(User(
        id=None,
        username="new_message_event2",
        hashed_password=password_provider.hash_password("123")
    ))
    chat = await chat_gateway.save_chat(Chat(
        id=None,
        title="Title",
        users_ids=[user1.id, user2.id],
    ))

    await transaction_manager.commit()

    response = client.post(
        r"/user/login",
        json={
            "username": user1.username,
            "password": "123",
        }
    )

    assert response.status_code == 200

    token = response.cookies["token"].strip('"')
    headers = {
        "Cookie": f"token={token}"
    }
    with client.websocket_connect(r"ws://localhost:8000/event/listen", headers=headers) as websocket:
        
        response = client.post(
            r"/message",
            json={
                "chat_id": chat.id,
                "text": "MessageText",
            }
        )

        assert response.status_code == 200

        response_json = response.json()

        assert websocket.receive_json() == {
            "event": "new_message",
            "message": response_json
        }
