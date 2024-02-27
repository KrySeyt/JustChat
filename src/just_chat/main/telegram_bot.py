import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from just_chat.main.ioc import UserIoC
from just_chat.presentation.telegram_bot import router


async def main() -> None:
    user_ioc = UserIoC()

    dispatcher = Dispatcher(
        user_ioc=user_ioc,
    )

    dispatcher.include_router(router)

    bot_token = getenv("BOT_TOKEN")

    if bot_token is None:
        raise ValueError

    bot = Bot(bot_token, parse_mode=ParseMode.HTML)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
