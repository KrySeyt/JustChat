import asyncio
from typing import Annotated

from fastapi import WebSocket, Depends
from starlette.websockets import WebSocketState

from just_chat.adapters.events.websocket_event_gateway import websockets, websockets_lock
from just_chat.application.common.id_provider import IdProvider
from just_chat.presentation.web_api.dependencies.stub import Stub
from just_chat.presentation.web_api.public.event import event_router


@event_router.websocket("/listen")
async def websocket_endpoint(
        websocket: WebSocket,
        id_provider: Annotated[IdProvider, Depends(Stub(IdProvider))],
) -> None:
    await websocket.accept()
    user_id = await id_provider.get_current_user_id()

    async with websockets_lock:  # Temp solution
        websockets[user_id] = websocket

    while websocket.client_state != WebSocketState.DISCONNECTED:
        await asyncio.sleep(1)

    async with websockets_lock:
        del websockets[user_id]
