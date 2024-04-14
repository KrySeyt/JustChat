from dataclasses import dataclass

from just_chat.message.domain.message import Message


@dataclass
class NewMessage:
    message: Message


class EventService:
    def create_new_message_event(self, message: Message) -> NewMessage:
        return NewMessage(message)
