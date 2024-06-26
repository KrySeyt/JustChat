import re
from typing import Any

from psycopg import AsyncConnection

from just_chat.common.adapters.sql_executor import SQLExecutor


class PsycopgSQLExecutor(SQLExecutor):
    def __init__(self, conn: AsyncConnection[Any]) -> None:
        self._conn = conn
        self._default_placeholder_pattern = re.compile(r":\w+")

    def _normalize_placeholder(self, placeholder: re.Match[str]) -> str:
        return f"%({placeholder.group(0)[1:]})s"

    def normalize_placeholders(self, query: str) -> str:
        return re.sub(
            self._default_placeholder_pattern,
            self._normalize_placeholder,
            query,
        )

    async def execute(self, query: str, values: dict[str, Any] | None = None) -> list[tuple[Any, ...]]:
        normalized_query = self.normalize_placeholders(query)
        values = values or {}
        async with self._conn.cursor() as cursor:
            await cursor.execute(normalized_query, values)

            if cursor.rownumber is None:
                return []

            result = await cursor.fetchall()
            return list(result)

    async def scalar(self, query: str, values: dict[str, Any] | None = None) -> Any:
        normalized_query = self.normalize_placeholders(query)
        values = values or {}
        async with self._conn.cursor() as cursor:
            await cursor.execute(normalized_query, values)
            row = await cursor.fetchone()
            return row[0] if row else None

    async def scalars(self, query: str, values: dict[str, Any] | None = None) -> list[Any]:
        normalized_query = self.normalize_placeholders(query)
        values = values or {}
        async with self._conn.cursor() as cursor:
            await cursor.execute(normalized_query, values)
            return [row[0] for row in await cursor.fetchall()]
