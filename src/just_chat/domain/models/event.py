from dataclasses import dataclass

from just_chat.domain.models.message import Message


@dataclass
class NewMessage:
    message: Message
