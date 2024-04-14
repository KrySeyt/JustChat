from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from just_chat.common.external.database.sql_models import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
