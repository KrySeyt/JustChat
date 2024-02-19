from just_chat.application.common.id_provider import IdProvider
from just_chat.application.common.session_gateway import SessionToken
from just_chat.application.user.get_user_by_token import GetUserIdByToken
from just_chat.domain.models.user import UserId


class SessionIdProvider(IdProvider):
    def __init__(self, token: SessionToken, user_id_provider: GetUserIdByToken) -> None:
        self._token = token
        self._user_id_provider = user_id_provider

    def get_current_user_id(self) -> UserId:
        return self._user_id_provider(self._token)
