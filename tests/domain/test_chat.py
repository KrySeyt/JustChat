from just_chat.chat.domain.chat import ChatService
from just_chat.user.domain.user import UserId


def test_create_chat():
    chat = ChatService().create_chat(
        title="Chat title",
        users_ids=[UserId(i) for i in range(3)],
    )

    assert chat.title == "Chat title"
    assert chat.users_ids == [0, 1, 2]
