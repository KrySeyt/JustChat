from collections.abc import Sequence
from dataclasses import asdict

from faststream.rabbit import ExchangeType, RabbitBroker, RabbitExchange, RabbitQueue

from just_chat.event.application.interfaces.event_bus import EventBus
from just_chat.event.application.interfaces.event_gateway import EventGateway
from just_chat.event.domain.event import NewMessage
from just_chat.user.domain.user import UserId


class RabbitEventGateway(EventGateway):
    def __init__(self, broker: RabbitBroker) -> None:
        self._broker = broker
        self._exchange = RabbitExchange(
            name="events",
            type=ExchangeType.FANOUT,
        )

    async def send_new_message_event(self, event: NewMessage, target_user_ids: Sequence[UserId]) -> None:
        await self._broker.declare_exchange(self._exchange)
        await self._broker.declare_queue(RabbitQueue(name="t"))

        await self._broker.publish(
            message={
                    "event": "new_message",
                    "user_ids": list(target_user_ids),
                    "message": asdict(event.message),
                },
            exchange=self._exchange,
        )

    async def add_user_event_bus(self, event_bus: EventBus, user_id: UserId) -> None:
        pass

    async def delete_user_event_bus(self, user_id: UserId) -> None:
        pass
