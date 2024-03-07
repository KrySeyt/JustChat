from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from just_chat.common.adapters.database.models import Base


class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str]


class ChatUserRelation(Base):
    __tablename__ = "chat_user_relation"

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "user.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        primary_key=True,
    )
    chat_id: Mapped[int] = mapped_column(
        ForeignKey(
            "chat.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        primary_key=True,
    )
