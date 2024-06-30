import asyncio
import os

from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitMessage

rabbit_url = os.getenv("RABBIT_URL")
broker = RabbitBroker(rabbit_url)
app = FastStream(broker)


@broker.subscriber(queue="", exchange="events")
async def event_handler(message: RabbitMessage) -> None:
    print(message.decoded_body)  # noqa: T201


async def main() -> None:
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
