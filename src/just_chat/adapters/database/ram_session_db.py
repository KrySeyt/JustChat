from just_chat.application.common.session_gateway import SessionGateway, SessionToken, SessionNotFound
from just_chat.domain.models.user import UserId


class RAMSessionGateway(SessionGateway):
    RAM_SESSION_DB: dict[SessionToken, UserId] = {}

    async def get_user_id(self, token: SessionToken) -> UserId:
        if token in self.RAM_SESSION_DB:
            return self.RAM_SESSION_DB[token]

        raise SessionNotFound

    async def save_session_token(self, user_id: UserId, token: SessionToken) -> None:
        self.RAM_SESSION_DB[token] = user_id
