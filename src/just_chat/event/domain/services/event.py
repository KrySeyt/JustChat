from just_chat.event.domain.models.event import NewMessage
from just_chat.message.domain.models.message import Message


class EventService:
    def create_new_message_event(self, message: Message) -> NewMessage:
        return NewMessage(message)
