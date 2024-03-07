from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from just_chat.chat.domain.models.chat import Chat
from just_chat.common.adapters.database.models import Base
from just_chat.user.domain.models.user import User


class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str]

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped[User] = relationship()

    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    owner: Mapped[User] = relationship()

    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id"))
    chat: Mapped[Chat] = relationship()
