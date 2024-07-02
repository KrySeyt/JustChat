import asyncio
import os
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.websockets import WebSocket, WebSocketState
from faststream.rabbit import RabbitBroker, RabbitMessage, ExchangeType, RabbitExchange

from just_chat.common.external.web.dependencies.stub import Stub
from just_chat.main.config import get_postgres_settings
from just_chat.main.ioc import UserIoC
from just_chat.user.adapters.interactor_factory import UserInteractorFactory
from just_chat.user.application.id_provider import IdProvider
from just_chat.user.external.web.dependencies.id_provider import get_session_id_provider

UserId = int

websockets: dict[UserId, WebSocket] = {}

fastapi = FastAPI()

# rabbit_url = os.getenv("RABBIT_URL")
# broker = RabbitBroker(rabbit_url)


@fastapi.websocket("/listen")
async def websocket_endpoint(
        websocket: WebSocket,
        id_provider: Annotated[IdProvider, Depends(Stub(IdProvider))],
):
    await websocket.accept()
    user_id = await id_provider.get_current_user_id()
    # websockets[user_id] = websocket
    print(user_id)

    while websocket.client_state != WebSocketState.DISCONNECTED:
        await asyncio.sleep(1)

    # del websockets[user_id]


# @fastapi.websocket("/listen")
# async def websocket_endpoint(
#         websocket: WebSocket,
#         # id_provider: Annotated[IdProvider, Depends(Stub(IdProvider))],
# ) -> None:
#     await websocket.accept()
#     # assert False, websocket
#     # user_id = await id_provider.get_current_user_id()
#     # websockets[user_id] = websocket
#
#     while websocket.client_state != WebSocketState.DISCONNECTED:
#         await asyncio.sleep(1)
#
#     # del websockets[user_id]


async def event_handler(message: RabbitMessage) -> None:
    data = message.decoded_body
    user_ids = data.pop("user_ids")

    for user_id in user_ids:
        ws = websockets.get(user_id, None)

        if ws:
            await ws.send_json(data)


# @asynccontextmanager
# async def lifespan(app: FastAPI) -> None:
#     exchange = RabbitExchange(
#         name="events",
#         type=ExchangeType.FANOUT,
#     )
#     async with broker:
#         await broker.declare_exchange(exchange)
#
#         yield


def create_app() -> FastAPI:
    # fastapi = FastAPI(lifespan=lifespan)

    postgres_settings = get_postgres_settings()
    user_ioc = UserIoC(postgres_settings.dsn)
    fastapi.dependency_overrides[UserInteractorFactory] = lambda: user_ioc
    fastapi.dependency_overrides[IdProvider] = get_session_id_provider

    # broker.subscriber(queue="", exchange="events")(event_handler)

    return fastapi


app = create_app()
