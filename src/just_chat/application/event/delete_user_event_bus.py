
from just_chat.application.common.event_bus import EventBus
from just_chat.application.common.event_gateway import EventGateway
from just_chat.application.common.id_provider import IdProvider
from just_chat.application.common.interactor import Interactor


class DeleteUserEventBus(Interactor[None, EventBus]):
    def __init__(self, event_gateway: EventGateway, id_provider: IdProvider) -> None:
        self._event_gateway = event_gateway
        self._id_provider = id_provider

    async def __call__(self, data: None = None) -> EventBus:
        user_id = await self._id_provider.get_current_user_id()
        return await self._event_gateway.delete_user_event_bus(user_id)
