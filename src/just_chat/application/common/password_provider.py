from abc import ABC, abstractmethod


class PasswordProvider(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify_password(self, password: str, target_hashed_password: str) -> bool:
        raise NotImplementedError
