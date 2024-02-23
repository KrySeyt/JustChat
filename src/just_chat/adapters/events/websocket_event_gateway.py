import asyncio
from dataclasses import asdict
from typing import Sequence

from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from just_chat.application.common.event_gateway import EventGateway
from just_chat.domain.models.event import NewMessage
from just_chat.domain.models.user import UserId

websockets: dict[int, WebSocket] = {}  # Temp solution
websockets_lock = asyncio.Lock()


class WSEventGateway(EventGateway):
    async def send_new_message_event(self, event: NewMessage, target_user_ids: Sequence[UserId]) -> None:
        async with websockets_lock:
            for user_id in target_user_ids:
                if user_id not in websockets:
                    continue

                websocket = websockets[user_id]

                try:
                    await websocket.send_json({
                        "event": "new_message",
                        "message": asdict(event.message)
                    })
                except WebSocketDisconnect:
                    pass
