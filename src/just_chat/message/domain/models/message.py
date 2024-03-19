from dataclasses import dataclass
from typing import NewType

from just_chat.chat.domain.models.chat import ChatId
from just_chat.user.domain.models.user import UserId

MessageId = NewType("MessageId", int)
FileUrl = str


@dataclass()
class Message:
    id: MessageId | None
    text: str
    author_id: UserId
    owner_id: UserId
    chat_id: ChatId
    image_url: FileUrl | None = None
