import threading
from dataclasses import asdict
from typing import Container

from just_chat.adapters.database.exceptions import UserNotFound
from just_chat.application.common.user_gateway import UserGateway
from just_chat.domain.models.user import UserId, User


class RAMUserGateway(UserGateway):
    RAM_USERS_DB: list[User] = []
    next_user_id = 0
    next_user_id_lock = threading.Lock()

    def save_user(self, user: User) -> User:
        user_in_db = User(
            **asdict(user) | {"id": self.next_user_id}
        )

        with self.next_user_id_lock:
            type(self).next_user_id += 1

        self.RAM_USERS_DB.append(user_in_db)

        return user_in_db

    def get_user_by_id(self, id_: UserId) -> User:
        for user in self.RAM_USERS_DB:
            if user.id == id_:
                return user

        raise UserNotFound(f"User with id {id_} not found")

    def get_user_by_username(self, username: str) -> User:
        for user in self.RAM_USERS_DB:
            if user.username == username:
                return user

        raise UserNotFound(f"User with username {username} not found")

    def get_random_user(self, exclude: Container[UserId]) -> User:
        for user in self.RAM_USERS_DB:
            if user.id not in exclude:
                return user

        raise UserNotFound("User not found")

    def delete_user_by_id(self, id_: UserId) -> User:
        user = self.get_user_by_id(id_)
        self.RAM_USERS_DB.remove(user)
        return user
