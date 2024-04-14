from just_chat.common.application.interactor import Interactor
from just_chat.common.application.transaction_manager import TransactionManager
from just_chat.event.application.interfaces.event_bus import EventBus
from just_chat.event.application.interfaces.event_gateway import EventGateway
from just_chat.user.application.id_provider import IdProvider


class AddUserEventBus(Interactor[EventBus, None]):
    def __init__(
            self,
            event_gateway: EventGateway,
            id_provider: IdProvider,
            transaction_manager: TransactionManager,
    ) -> None:
        self._event_gateway = event_gateway
        self._id_provider = id_provider
        self._transaction_manager = transaction_manager

    async def __call__(self, event_bus: EventBus) -> None:
        user_id = await self._id_provider.get_current_user_id()
        await self._event_gateway.add_user_event_bus(event_bus, user_id)
        await self._transaction_manager.commit()
