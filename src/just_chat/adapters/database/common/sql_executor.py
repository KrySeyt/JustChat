from abc import ABC, abstractmethod
from typing import Any


class SQLExecutor(ABC):
    @abstractmethod
    async def execute(self, query: str, values: dict[str, Any] | None = None) -> list[tuple[Any, ...]]:
        raise NotImplementedError

    @abstractmethod
    async def scalar(self, query: str, values: dict[str, Any] | None = None) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def scalars(self, query: str, values: dict[str, Any] | None = None) -> list[Any]:
        raise NotImplementedError
