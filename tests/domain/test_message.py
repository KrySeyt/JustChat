from just_chat.domain.models.chat import ChatId
from just_chat.domain.models.message import Message, MessageId
from just_chat.domain.models.user import UserId
from just_chat.domain.services.message import MessageService


def test_create_message():
    message = MessageService().create_message(
        text="Message text",
        chat_id=ChatId(1),
        author_id=UserId(3),
        owner_id=UserId(5),
    )

    assert message.id is None
    assert message.text == "Message text"
    assert message.chat_id == 1
    assert message.author_id == 3
    assert message.owner_id == 5


def test_update_message():
    message = Message(
        id=MessageId(16),
        text="Message text",
        chat_id=ChatId(1),
        author_id=UserId(3),
        owner_id=UserId(5),
    )

    updated_message = MessageService().update_message(message, "New text")

    assert updated_message.id == 16
    assert updated_message.text == "New text"
    assert updated_message.chat_id == 1
    assert updated_message.author_id == 3
    assert updated_message.owner_id == 5

