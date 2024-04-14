from just_chat.user.application.interfaces.session_gateway import SessionGateway, SessionNotFoundError, SessionToken
from just_chat.user.domain.user import UserId

RAM_SESSION_DB: dict[SessionToken, UserId] = {}


class RAMSessionGateway(SessionGateway):

    async def get_user_id(self, token: SessionToken) -> UserId:
        if token in RAM_SESSION_DB:
            return RAM_SESSION_DB[token]

        raise SessionNotFoundError

    async def save_session_token(self, user_id: UserId, token: SessionToken) -> None:
        RAM_SESSION_DB[token] = user_id
