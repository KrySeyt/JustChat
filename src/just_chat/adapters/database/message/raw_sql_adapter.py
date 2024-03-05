from typing import Any

from just_chat.adapters.database.common.sql_executor import SQLExecutor
from just_chat.application.common.message_gateway import MessageGateway, MessageNotFoundError
from just_chat.domain.models.chat import ChatId
from just_chat.domain.models.message import Message, MessageId


class RawSQLMessageGateway(MessageGateway):
    def __init__(self, sql_executor: SQLExecutor) -> None:
        self._sql_executor = sql_executor

    async def save_message(self, message: Message) -> Message:
        message_id_placeholder = ":message_id" if message.id is not None else "NEXTVAL('message_id_seq')"
        q_save_message = f"""
            INSERT INTO message(
                id,
                text,
                author_id,
                owner_id,
                chat_id
            )
            VALUES (
                {message_id_placeholder},
                :text,
                :author_id,
                :owner_id,
                :chat_id
            )
            ON CONFLICT (id)
            DO UPDATE
            SET
            text = :text,
            author_id = :author_id,
            owner_id = :owner_id,
            chat_id = :chat_id
            RETURNING
            id,
            text,
            author_id,
            owner_id,
            chat_id
        """

        values: dict[str, Any] = {
            "message_id": message.id,
            "text": message.text,
            "author_id": message.author_id,
            "owner_id": message.owner_id,
            "chat_id": message.chat_id,
        }

        messages_datas = await self._sql_executor.execute(q_save_message, values)

        message_data, = messages_datas
        return Message(*message_data)

    async def get_message_by_id(self, id_: MessageId) -> Message:
        q_get_message_by_id = """
        SELECT
        message.id,
        message.text,
        message.author_id,
        message.owner_id,
        message.chat_id
        FROM message
        WHERE message.id = :message_id
        """

        values: dict[str, Any] = {
            "message_id": id_,
        }

        messages_datas = await self._sql_executor.execute(q_get_message_by_id, values)

        if not messages_datas:
            raise MessageNotFoundError

        return Message(*messages_datas[0])

    async def get_chat_messages_by_chat_id(self, chat_id: ChatId) -> list[Message]:
        q_get_message_by_id = """
        SELECT
        message.id,
        message.text,
        message.author_id,
        message.owner_id,
        message.chat_id
        FROM message
        WHERE message.chat_id = :chat_id
        """

        values: dict[str, Any] = {
            "chat_id": chat_id,
        }

        messages_datas = await self._sql_executor.execute(q_get_message_by_id, values)

        return [Message(*data) for data in messages_datas]
