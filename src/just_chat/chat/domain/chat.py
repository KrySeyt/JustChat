from collections.abc import Sequence
from dataclasses import dataclass
from typing import NewType

from just_chat.user.domain.user import UserId

ChatId = NewType("ChatId", int)


@dataclass()
class Chat:
    id: ChatId | None
    title: str
    users_ids: list[UserId]


class ChatService:
    def create_chat(self, title: str, users_ids: Sequence[UserId]) -> Chat:
        return Chat(
            id=None,
            title=title,
            users_ids=list(users_ids),
        )
