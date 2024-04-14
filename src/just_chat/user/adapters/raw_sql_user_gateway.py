from typing import Any

from just_chat.common.adapters.sql_executor import SQLExecutor
from just_chat.user.application.interfaces.user_gateway import UserGateway, UserNotFoundError
from just_chat.user.domain.user import User, UserId


class RawSQLUserGateway(UserGateway):
    def __init__(self, sql_executor: SQLExecutor) -> None:
        self._sql_executor = sql_executor

    async def save_user(self, user: User) -> User:
        user_id_placeholder = ":user_id" if user.id is not None else "NEXTVAL('user_id_seq')"
        q_save_user = f"""
            INSERT INTO "user"(id, username, hashed_password)
            VALUES ({user_id_placeholder}, :username, :hashed_password)
            ON CONFLICT (id)
            DO UPDATE
            SET
            username = :username
            RETURNING "user".id, "user".username, "user".hashed_password
        """

        values: dict[str, Any] = {
            "user_id": user.id,
            "username": user.username,
            "hashed_password": user.hashed_password,
        }

        users_datas = await self._sql_executor.execute(q_save_user, values)

        user_data, = users_datas
        return User(*user_data)

    async def get_user_by_id(self, id_: UserId) -> User:
        q_get_chat_by_id = """
        SELECT "user".id, "user".username, "user".hashed_password
        FROM "user"
        WHERE "user".id = :user_id
        """

        values: dict[str, Any] = {
            "user_id": id_,
        }

        users_datas = await self._sql_executor.execute(q_get_chat_by_id, values)

        if not users_datas:
            raise UserNotFoundError

        return User(*users_datas[0])

    async def get_user_by_username(self, username: str) -> User:
        q_get_chat_by_id = """
        SELECT "user".id, "user".username, "user".hashed_password
        FROM "user"
        WHERE "user".username = :username
        """
        values: dict[str, Any] = {
            "username": username,
        }

        users_datas = await self._sql_executor.execute(q_get_chat_by_id, values)

        if not users_datas:
            raise UserNotFoundError

        return User(*users_datas[0])

    async def delete_user_by_id(self, id_: UserId) -> User:
        q_delete_chat_by_id = """
        DELETE FROM "user"
        WHERE "user".id = :user_id
        RETURNING "user".id, "user".username
        """
        values: dict[str, Any] = {
            "user_id": id_,
        }

        users_datas = await self._sql_executor.execute(q_delete_chat_by_id, values)

        if not users_datas:
            raise UserNotFoundError

        return User(*users_datas[0])

