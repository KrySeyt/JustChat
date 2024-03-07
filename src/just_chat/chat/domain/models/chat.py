from dataclasses import dataclass
from typing import NewType

from just_chat.user.domain.models.user import UserId

ChatId = NewType("ChatId", int)


@dataclass()
class Chat:
    id: ChatId | None
    title: str
    users_ids: list[UserId]
