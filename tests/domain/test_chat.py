from just_chat.domain.models.user import UserId
from just_chat.domain.services.chat import ChatService


def test_create_chat():
    chat = ChatService().create_chat(
        title="Chat title",
        users_ids=[UserId(i) for i in range(3)],
    )

    assert chat.title == "Chat title"
    assert chat.users_ids == [0, 1, 2]
