from just_chat.common.application.interactor import Interactor
from just_chat.user.application.interfaces.session_gateway import SessionGateway, SessionToken
from just_chat.user.domain.user import UserId


class GetUserIdByToken(Interactor[SessionToken, UserId]):
    def __init__(self, session_gateway: SessionGateway) -> None:
        self._session_gateway = session_gateway

    async def __call__(self, data: SessionToken) -> UserId:
        return await self._session_gateway.get_user_id(token=data)
