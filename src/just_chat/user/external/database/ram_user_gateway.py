import asyncio
from collections.abc import Container
from dataclasses import asdict

from just_chat.user.application.interfaces.user_gateway import UserGateway, UserNotFoundError
from just_chat.user.domain.user import User, UserId

RAM_USERS_DB: list[User] = []


class RAMUserGateway(UserGateway):
    next_user_id = 0
    next_user_id_lock = asyncio.Lock()

    async def save_user(self, user: User) -> User:
        async with self.next_user_id_lock:
            user_in_db = User(
                **asdict(user) | {"id": self.next_user_id},
            )
            type(self).next_user_id += 1

        RAM_USERS_DB.append(user_in_db)

        return user_in_db

    async def get_user_by_id(self, id_: UserId) -> User:
        for user in RAM_USERS_DB:
            if user.id == id_:
                return user

        raise UserNotFoundError(f"User with id {id_} not found")

    async def get_user_by_username(self, username: str) -> User:
        for user in RAM_USERS_DB:
            if user.username == username:
                return user

        raise UserNotFoundError(f"User with username {username} not found")

    async def get_random_user(self, exclude: Container[UserId]) -> User:
        for user in RAM_USERS_DB:
            if user.id not in exclude:
                return user

        raise UserNotFoundError("User not found")

    async def delete_user_by_id(self, id_: UserId) -> User:
        user = await self.get_user_by_id(id_)
        RAM_USERS_DB.remove(user)
        return user
