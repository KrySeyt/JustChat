from just_chat.common.application.transaction_manager import TransactionManager


class RAMTransactionManager(TransactionManager):
    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass
