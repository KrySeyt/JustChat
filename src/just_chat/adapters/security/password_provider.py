
from passlib.ifc import PasswordHash

from just_chat.application.common.password_provider import PasswordProvider


class HashingPasswordProvider(PasswordProvider):
    def __init__(self, hasher: PasswordHash | type[PasswordHash]) -> None:
        self._hasher = hasher

    def hash_password(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify_password(self, password: str, target_hashed_password: str) -> bool:
        return bool(self._hasher.verify(password, target_hashed_password))
