import asyncio
from typing import Annotated, Any

from fastapi import Depends, WebSocket
from starlette.websockets import WebSocketDisconnect, WebSocketState

from just_chat.common.external.web.dependencies.stub import Stub
from just_chat.event.adapters.interactor_factory import EventInteractorFactory
from just_chat.event.application.interfaces.event_bus import ConnectionClosedError, EventBus
from just_chat.event.external.web.public.router import event_router
from just_chat.user.application.id_provider import IdProvider


class WebsocketEventBus(EventBus):
    def __init__(self, websocket: WebSocket) -> None:
        self._websocket = websocket

    async def send_json(self, data: Any) -> None:
        try:
            await self._websocket.send_json(data)
        except WebSocketDisconnect as err:
            raise ConnectionClosedError from err


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
