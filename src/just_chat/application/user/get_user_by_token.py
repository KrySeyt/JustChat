from just_chat.application.common.interactor import Interactor
from just_chat.application.common.session_gateway import SessionGateway, SessionToken
from just_chat.domain.models.user import UserId


class GetUserIdByToken(Interactor[SessionToken, UserId]):
    def __init__(self, session_gateway: SessionGateway) -> None:
        self._session_gateway = session_gateway

    async def __call__(self, data: SessionToken) -> UserId:
        user_id = await self._session_gateway.get_user_id(token=data)
        return user_id
