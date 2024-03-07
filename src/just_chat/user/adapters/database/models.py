from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from just_chat.common.adapters.database.models import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str]
    hashed_password: Mapped[str]
