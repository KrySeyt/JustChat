from just_chat.common.application.transaction_manager import TransactionManager


class TransactionManagerStub(TransactionManager):
    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass
