from dataclasses import dataclass
from typing import NewType

from .chat import ChatId
from .user import UserId

MessageId = NewType("MessageId", int)


@dataclass()
class Message:
    id: MessageId | None
    text: str
    author_id: UserId
    owner_id: UserId
    chat_id: ChatId
