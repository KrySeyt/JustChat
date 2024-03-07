from just_chat.user.application.gateways.session_gateway import SessionToken
from just_chat.user.application.get_user_by_token import GetUserIdByToken
from just_chat.user.application.id_provider import IdProvider
from just_chat.user.domain.models.user import UserId


class SessionIdProvider(IdProvider):
    def __init__(self, token: SessionToken, user_id_provider: GetUserIdByToken) -> None:
        self._token = token
        self._user_id_provider = user_id_provider

    async def get_current_user_id(self) -> UserId:
        return await self._user_id_provider(self._token)
