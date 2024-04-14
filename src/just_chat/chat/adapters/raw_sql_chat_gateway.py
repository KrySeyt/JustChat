from typing import Any

from just_chat.chat.application.interfaces.chat_gateway import ChatGateway, ChatNotFoundError
from just_chat.chat.domain.chat import Chat, ChatId
from just_chat.common.adapters.sql_executor import SQLExecutor
from just_chat.user.application.interfaces.user_gateway import UserNotFoundError
from just_chat.user.domain.user import UserId


class RawSQLChatGateway(ChatGateway):
    def __init__(self, sql_executor: SQLExecutor) -> None:
        self._sql_executor = sql_executor

    async def save_chat(self, chat: Chat) -> Chat:
        chat_id_placeholder = ":chat_id" if chat.id is not None else "NEXTVAL('chat_id_seq')"
        q_save_chat = f"""
            INSERT INTO chat(id, title)
            VALUES ({chat_id_placeholder}, :title)
            ON CONFLICT (id)
            DO UPDATE
            SET
            title = :title
            RETURNING chat.id, chat.title
        """

        values: dict[str, Any] = {
            "chat_id": chat.id,
            "title": chat.title,
        }

        chats_datas = await self._sql_executor.execute(q_save_chat, values)

        users_ids = []
        if chat.users_ids:
            q_delete_extra_users_from_chat = """
                DELETE FROM chat_user_relation
                WHERE chat_id = :chat_id
                AND
                user_id in (
            """

            delete_users_values: dict[str, Any] = {
                "chat_id": chat.id,
            }

            for i, user_id in enumerate(chat.users_ids):
                q_delete_extra_users_from_chat += f":user_id{i}, "
                delete_users_values[f"user_id{i}"] = user_id

            q_delete_extra_users_from_chat = q_delete_extra_users_from_chat.rstrip(", ") + ")"
            await self._sql_executor.execute(q_delete_extra_users_from_chat, delete_users_values)

            q_users_exists = f"""
            SELECT COUNT("user".id) = {len(chat.users_ids)} FROM "user" WHERE "user".id in
            ({", ".join(str(i) for i in chat.users_ids)})
            """

            values = {
                "users_ids": tuple(chat.users_ids),
            }

            if not await self._sql_executor.scalar(q_users_exists, values):
                raise UserNotFoundError

            relations_values: dict[str, Any] = {}
            q_create_chat_user_relations = "INSERT INTO chat_user_relation(user_id, chat_id) VALUES"
            for i, user_id in enumerate(chat.users_ids):
                q_create_chat_user_relations += f"(:user_id{i}, :chat_id),"
                relations_values[f"user_id{i}"] = user_id

            q_create_chat_user_relations = q_create_chat_user_relations.strip(",")
            q_create_chat_user_relations += " RETURNING user_id"

            relations_values["chat_id"] = chats_datas[0][0]

            users_ids = await self._sql_executor.scalars(q_create_chat_user_relations, relations_values)


        chat_data, = chats_datas
        return Chat(id=chat_data[0], title=chat_data[1], users_ids=users_ids)

    async def create_chat_with_random_user(self, title: str, user_id: UserId) -> Chat:
        q_get_occupied_users_ids = """
            SELECT DISTINCT l2.user_id FROM chat_user_relation
            JOIN chat_user_relation l1 ON l1.user_id = :user_id
            JOIN chat_user_relation l2 ON l2.chat_id = l1.chat_id;
        """

        get_occupied_users_values = {
            "user_id": user_id,
        }

        occupied_users_ids = await self._sql_executor.scalars(q_get_occupied_users_ids, get_occupied_users_values)
        occupied_users_ids = occupied_users_ids or []

        q_get_user_id = """
            SELECT
            "user".id
            FROM "user"
        """

        q_get_user_id += f"""
            WHERE "user".id NOT IN ({", ".join(str(i) for i in (*occupied_users_ids, user_id))})
            LIMIT 1
        """

        second_user_id = await self._sql_executor.scalar(q_get_user_id)

        if second_user_id is None:
            raise UserNotFoundError

        chat = Chat(
            id=None,
            title=title,
            users_ids=[user_id, second_user_id],
        )

        return await self.save_chat(chat)

    async def get_chat_by_id(self, id_: ChatId) -> Chat:
        q_get_chat_by_id = "SELECT chat.id, chat.title FROM chat WHERE chat.id = :chat_id"
        chat_values: dict[str, Any] = {
            "chat_id": id_,
        }

        chats_datas = await self._sql_executor.execute(q_get_chat_by_id, chat_values)

        if not chats_datas:
            raise ChatNotFoundError

        q_get_users_ids = "SELECT user_id FROM chat_user_relation WHERE chat_id = :chat_id"
        users_values: dict[str, Any] = {
            "chat_id": id_,
        }
        users_ids = await self._sql_executor.scalars(q_get_users_ids, users_values)

        chat_data, = chats_datas
        return Chat(id=chat_data[0], title=chat_data[1], users_ids=users_ids)

    async def delete_chat_by_id(self, id_: ChatId) -> Chat:
        q_get_users_ids = "SELECT user_id FROM chat_user_relation WHERE chat_id = :chat_id"
        users_values: dict[str, Any] = {
            "chat_id": id_,
        }

        users_ids = await self._sql_executor.scalars(q_get_users_ids, users_values)

        q_delete_chat_by_id = """
        DELETE FROM chat
        WHERE chat.id = :chat_id
        RETURNING chat.id, chat.title
        """
        chat_values: dict[str, Any] = {
            "chat_id": id_,
        }

        chats_datas = await self._sql_executor.execute(q_delete_chat_by_id, chat_values)

        if not chats_datas:
            raise ChatNotFoundError

        chat_data, = chats_datas

        return Chat(id=chat_data[0], title=chat_data[1], users_ids=users_ids)
