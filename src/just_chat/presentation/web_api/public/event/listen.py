import asyncio
from typing import Annotated, Any

from fastapi import WebSocket, Depends
from starlette.websockets import WebSocketState, WebSocketDisconnect

from just_chat.application.common.event_bus import EventBus, ConnectionClosed
from just_chat.application.common.id_provider import IdProvider
from just_chat.presentation.interactor_factory.event import EventInteractorFactory
from just_chat.presentation.web_api.dependencies.stub import Stub
from just_chat.presentation.web_api.public.event import event_router


class WebsocketEventBus(EventBus):
    def __init__(self, websocket: WebSocket) -> None:
        self._websocket = websocket

    async def send_json(self, data: Any) -> None:
        try:
            await self._websocket.send_json(data)
        except WebSocketDisconnect:
            raise ConnectionClosed


@event_router.websocket("/listen")
async def websocket_endpoint(
        interactor_factory: Annotated[EventInteractorFactory, Depends()],
        websocket: WebSocket,
        id_provider: Annotated[IdProvider, Depends(Stub(IdProvider))],
) -> None:
    await websocket.accept()

    async with interactor_factory.add_user_event_bus(id_provider) as add_bus_interactor:
        await add_bus_interactor(WebsocketEventBus(websocket))

    while websocket.client_state != WebSocketState.DISCONNECTED:
        await asyncio.sleep(1)

    async with interactor_factory.delete_user_event_bus(id_provider) as delete_bus_interactor:
        await delete_bus_interactor()