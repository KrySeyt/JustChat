from collections.abc import Sequence

from just_chat.chat.domain.models.chat import Chat
from just_chat.user.domain.models.user import UserId


class ChatService:
    def create_chat(self, title: str, users_ids: Sequence[UserId]) -> Chat:
        return Chat(
            id=None,
            title=title,
            users_ids=list(users_ids),
        )
