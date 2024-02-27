from collections.abc import Sequence
from contextlib import suppress
from dataclasses import asdict

from just_chat.application.common.event_bus import ConnectionClosedError, EventBus
from just_chat.application.common.event_gateway import EventGateway
from just_chat.domain.models.event import NewMessage
from just_chat.domain.models.user import UserId

EVENT_BUS_DB: dict[UserId, EventBus] = {}


class WSEventGateway(EventGateway):
    async def send_new_message_event(self, event: NewMessage, target_user_ids: Sequence[UserId]) -> None:
        for user_id in target_user_ids:
            bus = EVENT_BUS_DB.get(user_id)

            if bus is None:
                continue

            with suppress(ConnectionClosedError):
                await bus.send_json({
                    "event": "new_message",
                    "message": asdict(event.message),
                })

    async def add_user_event_bus(self, event_bus: EventBus, user_id: UserId) -> None:
        EVENT_BUS_DB[user_id] = event_bus

    async def delete_user_event_bus(self, user_id: UserId) -> EventBus:
        return EVENT_BUS_DB.pop(user_id)
