from typing import Any

from psycopg import AsyncConnection

from just_chat.common.application.transaction_manager import TransactionManager


class PsycopgTransactionManager(TransactionManager):
    def __init__(self, conn: AsyncConnection[Any]) -> None:
        self._conn = conn

    async def commit(self) -> None:
        await self._conn.commit()

    async def rollback(self) -> None:
        await self._conn.rollback()
