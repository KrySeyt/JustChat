from just_chat.chat.domain.chat import Chat
from just_chat.common.domain.exceptions import DomainError
from just_chat.user.domain.user import UserId


class AccessDeniedError(DomainError):
    pass


class ChatAccessService:
    def ensure_user_can_write_to_chat(self, chat: Chat, user_id: UserId) -> None:
        if user_id not in chat.users_ids:
            raise AccessDeniedError
