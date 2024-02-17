import threading
from dataclasses import asdict

from just_chat.adapters.database.exceptions import ChatNotFound
from just_chat.application.common.chat_gateway import ChatGateway
from just_chat.domain.models.chat import ChatId, Chat


class RAMChatGateway(ChatGateway):
    RAM_CHATS_DB: list[Chat] = []
    next_chat_id = 0
    next_chat_id_lock = threading.Lock()

    def save_chat(self, chat: Chat) -> Chat:
        chat_in_db = Chat(
            **asdict(chat) | {"id": self.next_chat_id}
        )

        with self.next_chat_id_lock:
            type(self).next_chat_id += 1

        self.RAM_CHATS_DB.append(chat_in_db)

        return chat_in_db

    def get_chat_by_id(self, id_: ChatId) -> Chat:
        for chat in self.RAM_CHATS_DB:
            if chat.id == id_:
                return chat

        raise ChatNotFound(f"Chat with id {id_} not found")

    def delete_chat_by_id(self, id_: ChatId) -> Chat:
        chat = self.get_chat_by_id(id_)
        self.RAM_CHATS_DB.remove(chat)
        return chat
