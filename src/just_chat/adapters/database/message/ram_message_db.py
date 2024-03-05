import asyncio
from dataclasses import asdict

from just_chat.application.common.message_gateway import MessageGateway, MessageNotFoundError
from just_chat.domain.models.chat import ChatId
from just_chat.domain.models.message import Message, MessageId

RAM_MESSAGES_DB: list[Message] = []


class RAMMessageGateway(MessageGateway):
    next_message_id = 0
    next_message_id_lock = asyncio.Lock()

    async def save_message(self, message: Message) -> Message:
        async with self.next_message_id_lock:
            message_in_db = Message(
                **asdict(message) | {"id": self.next_message_id},
            )
            type(self).next_message_id += 1

        RAM_MESSAGES_DB.append(message_in_db)

        return message_in_db

    async def get_message_by_id(self, id_: MessageId) -> Message:
        for message in RAM_MESSAGES_DB:
            if message.id == id_:
                return message

        raise MessageNotFoundError(f"Message with id {id_} not found")

    async def get_chat_messages_by_chat_id(self, chat_id: ChatId) -> list[Message]:
        return [message for message in RAM_MESSAGES_DB if message.chat_id == chat_id]
