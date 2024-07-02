from redis.asyncio import Redis

from just_chat.user.application.interfaces.session_gateway import (
    SessionGateway,
    SessionNotFoundError,
    SessionToken,
)
from just_chat.user.domain.user import UserId


class RedisSessionGateway(SessionGateway):
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def get_user_id(self, token: SessionToken) -> UserId:
        user_id: bytes = await self._redis.get(token)

        if not user_id:
            raise SessionNotFoundError

        return UserId(int(user_id))

    async def save_session_token(self, user_id: UserId, token: SessionToken) -> None:
        await self._redis.set(
            name=token,
            value=user_id,
        )
