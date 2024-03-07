from just_chat.chat.domain.models.chat import ChatId
from just_chat.message.domain.models.message import Message
from just_chat.user.domain.models.user import UserId


class MessageService:
    def create_message(self, text: str, chat_id: ChatId, author_id: UserId, owner_id: UserId) -> Message:
        return Message(
            id=None,
            text=text,
            author_id=author_id,
            owner_id=owner_id,
            chat_id=chat_id,
        )

    def update_message(self, message: Message, new_text: str) -> Message:
        return Message(
            id=message.id,
            text=new_text,
            author_id=message.author_id,
            owner_id=message.owner_id,
            chat_id=message.chat_id,
        )
