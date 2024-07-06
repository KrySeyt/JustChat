import asyncio
import os
from collections.abc import AsyncGenerator, Iterable
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect, WebSocketState
from faststream.rabbit import ExchangeType, RabbitBroker, RabbitExchange, RabbitMessage

from just_chat.common.external.web.dependencies.stub import Stub
from just_chat.main.config import get_postgres_settings, get_redis_config
from just_chat.main.ioc import UserIoC
from just_chat.user.adapters.interactor_factory import UserInteractorFactory
from just_chat.user.application.id_provider import IdProvider
from just_chat.user.external.web.dependencies.id_provider import get_session_id_provider

UserId = int

websockets: dict[UserId, WebSocket] = {}


async def websocket_endpoint(
        websocket: WebSocket,
        id_provider: Annotated[IdProvider, Depends(Stub(IdProvider))],
) -> None:
    await websocket.accept()
    user_id = await id_provider.get_current_user_id()
    websockets[user_id] = websocket

    while websocket.client_state != WebSocketState.DISCONNECTED:
        await asyncio.sleep(1)

    del websockets[user_id]


async def event_handler(message: RabbitMessage) -> None:
    data = message.decoded_body
    assert isinstance(data, dict)

    user_ids = data.pop("user_ids")
    assert isinstance(user_ids, Iterable)

    for user_id in user_ids:
        assert isinstance(user_id, int)

        ws = websockets.get(user_id)

        if ws:
            try:
                await ws.send_json(data)
            except WebSocketDisconnect:
                del websockets[user_id]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with app.state.rabbit_broker:
        await app.state.rabbit_broker.start()
        yield


def create_app() -> FastAPI:
    fastapi = FastAPI(lifespan=lifespan)
    fastapi.websocket(path="/")(websocket_endpoint)

    postgres_settings = get_postgres_settings()
    redis_settings = get_redis_config()

    user_ioc = UserIoC(postgres_settings.dsn, redis_settings)
    fastapi.dependency_overrides[UserInteractorFactory] = lambda: user_ioc
    fastapi.dependency_overrides[IdProvider] = get_session_id_provider

    rabbit_url = os.getenv("RABBIT_URL")

    rabbit_broker = RabbitBroker(rabbit_url)
    exchange = RabbitExchange(name="events", type=ExchangeType.FANOUT)
    rabbit_broker.subscriber(queue="", exchange=exchange)(event_handler)

    fastapi.state.rabbit_broker = rabbit_broker

    return fastapi


app = create_app()
