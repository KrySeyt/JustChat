from just_chat.chat.domain.exceptions.access import AccessDeniedError
from just_chat.chat.domain.models.chat import Chat
from just_chat.user.domain.models.user import UserId


class ChatAccessService:
    def ensure_user_can_write_to_chat(self, chat: Chat, user_id: UserId) -> None:
        if user_id not in chat.users_ids:
            raise AccessDeniedError
