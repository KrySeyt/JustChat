from typing import Sequence

from ..models.chat import Chat
from ..models.user import UserId


class ChatService:
    def create_chat(self, title: str, users_ids: Sequence[UserId]) -> Chat:
        return Chat(
            id=None,
            title=title,
            users_ids=list(users_ids),
        )
