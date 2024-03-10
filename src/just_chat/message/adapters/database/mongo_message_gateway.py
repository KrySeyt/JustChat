from dataclasses import asdict

from motor.motor_asyncio import AsyncIOMotorDatabase

from just_chat.chat.domain.models.chat import ChatId
from just_chat.message.application.gateways.message_gateway import MessageGateway, MessageNotFoundError
from just_chat.message.domain.models.message import Message, MessageId


class MongoMessageGateway(MessageGateway):
    def __init__(self, conn: AsyncIOMotorDatabase) -> None:
        self._conn = conn

    async def save_message(self, message: Message) -> Message:
        await self._conn["message_max_id"].update_one({}, {"$inc": {"id": 1}}, upsert=True)

        id_data = await self._conn["message_max_id"].find_one()  # type: ignore[func-returns-value]
        assert id_data is not None
        id_ = id_data["id"]

        message.id = id_

        message_data = asdict(message)
        message_data["_id"] = message_data.pop("id")

        await self._conn["message"].insert_one(message_data)
        return message

    async def get_message_by_id(self, id_: MessageId) -> Message:
        message_data = await self._conn["message"].find_one({"_id": id_})  # type: ignore[func-returns-value]

        if not message_data:
            raise MessageNotFoundError

        message_data = dict(message_data)

        message_data["id"] = message_data.pop("_id")

        return Message(**message_data)

    async def get_chat_messages_by_chat_id(self, chat_id: ChatId) -> list[Message]:
        messages_cursor = self._conn["message"].find({"chat_id": chat_id})
        messages: list[Message] = []
        async for data in messages_cursor:  # type: ignore[var-annotated]
            data["id"] = data.pop("_id")
            messages.append(Message(**data))

        return messages
