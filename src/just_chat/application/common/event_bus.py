from abc import ABC, abstractmethod
from typing import Any


class ConnectionClosedError(Exception):
    pass


class EventBus(ABC):
    @abstractmethod
    async def send_json(self, data: Any) -> None:
        raise NotImplementedError
