import asyncio
from dataclasses import asdict

from just_chat.adapters.database.ram_user_db import RAM_USERS_DB
from just_chat.application.common.chat_gateway import ChatGateway, ChatNotFoundError
from just_chat.application.common.user_gateway import UserNotFoundError
from just_chat.domain.models.chat import Chat, ChatId
from just_chat.domain.models.user import UserId

RAM_CHATS_DB: list[Chat] = []


class RAMChatGateway(ChatGateway):
    next_chat_id = 0
    next_chat_id_lock = asyncio.Lock()

    async def save_chat(self, chat: Chat) -> Chat:
        async with self.next_chat_id_lock:
            chat_in_db = Chat(
                **asdict(chat) | {"id": self.next_chat_id},
            )
            type(self).next_chat_id += 1

        RAM_CHATS_DB.append(chat_in_db)

        return chat_in_db

    async def create_chat_with_random_user(self, title: str, user_id: UserId) -> Chat:
        excluded_users_ids = {user_id}
        for chat in RAM_CHATS_DB:
            if user_id in chat.users_ids:
                excluded_users_ids.union(chat.users_ids)

        for user in RAM_USERS_DB:
            assert user.id is not None

            if user.id in excluded_users_ids:
                continue

            async with self.next_chat_id_lock:
                chat = Chat(
                    id=ChatId(self.next_chat_id),
                    title=title,
                    users_ids=[user_id, user.id],
                )
                type(self).next_chat_id += 1
                RAM_CHATS_DB.append(chat)

            return chat

        raise UserNotFoundError

    async def get_chat_by_id(self, id_: ChatId) -> Chat:
        for chat in RAM_CHATS_DB:
            if chat.id == id_:
                return chat

        raise ChatNotFoundError(f"Chat with id {id_} not found")

    async def delete_chat_by_id(self, id_: ChatId) -> Chat:
        chat = await self.get_chat_by_id(id_)
        RAM_CHATS_DB.remove(chat)
        return chat
