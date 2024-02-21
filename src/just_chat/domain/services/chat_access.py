from ..exceptions.access import AccessDenied
from ..models.chat import Chat
from ..models.user import UserId


class ChatAccessService:
    def ensure_user_can_write_to_chat(self, chat: Chat, user_id: UserId) -> None:
        if user_id not in chat.users_ids:
            raise AccessDenied
