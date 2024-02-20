import threading
from dataclasses import asdict

from just_chat.application.common.message_gateway import MessageGateway, MessageNotFound
from just_chat.domain.models.message import Message, MessageId


class RAMMessageGateway(MessageGateway):
    RAM_MESSAGES_DB: list[Message] = []
    next_message_id = 0
    next_message_id_lock = threading.Lock()

    def save_message(self, message: Message) -> Message:
        with self.next_message_id_lock:
            message_in_db = Message(
                **asdict(message) | {"id": self.next_message_id}
            )
            type(self).next_message_id += 1

        self.RAM_MESSAGES_DB.append(message_in_db)

        return message_in_db

    def get_message_by_id(self, id_: MessageId) -> Message:
        for message in self.RAM_MESSAGES_DB:
            if message.id == id_:
                return message

        raise MessageNotFound(f"Message with id {id_} not found")
