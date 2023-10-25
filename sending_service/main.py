import asyncio
import random

from aio_pika import connect_robust
from aio_pika.patterns import RPC

from models import ServiceMessage, Mode
from settings import SendSettings, send_settings


def random_phones() -> list[int]:
    return [random.randint(0, 200) for _ in range(10)]


async def rpc_call(rabbit_url: str, mode: Mode | None = None) -> None:

    connection = await connect_robust(
        rabbit_url,
        client_properties={"connection_name": "caller"},
    )

    async with connection:
        channel = await connection.channel()
        rpc = await RPC.create(channel)

        for i in range(100):
            mode = mode or random.choice([Mode.ACCURATE, Mode.FAST])
            try:
                print(await rpc.proxy.get_phones_data(message=ServiceMessage(phones=random_phones(), mode=mode)))
            except TypeError as e:
                print(e)


async def main(settings: SendSettings = send_settings) -> None:
    await asyncio.gather(*[rpc_call(rabbit_url=settings.rabbitmq_url, mode=settings.HARD_MODE) for _ in range(10)])


if __name__ == "__main__":
    asyncio.run(main())
