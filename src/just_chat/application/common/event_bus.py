from abc import abstractmethod, ABC
from typing import Any


class ConnectionClosed(Exception):
    pass


class EventBus(ABC):
    @abstractmethod
    async def send_json(self, data: Any) -> None:
        raise NotImplementedError
