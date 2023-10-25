import asyncio

from aio_pika import connect_robust
from aio_pika.patterns import RPC

from models import ServiceMessage, Mode
from settings import SendSettings, send_settings

import random


def random_phones() -> list[int]:
    return [random.randint(0, 200) for _ in range(10)]


async def rpc_call(rpc: RPC, mode: Mode | None = None) -> None:
    for i in range(100):
        mode = mode or random.choice([Mode.ACCURATE, Mode.FAST])
        message = ServiceMessage(phones=random_phones(), mode=mode)
        try:
            print(await rpc.proxy.get_phones_data(message=message.model_dump_json()))
        except TypeError as e:
            print(e)


async def main(settings: SendSettings = send_settings) -> None:
    connection = await connect_robust(
        settings.rabbitmq_url,
        client_properties={"connection_name": "caller"},
    )

    async with connection:
        # Creating channel
        channel = await connection.channel()

        rpc = await RPC.create(channel)

        # Creates tasks by proxy object
        await asyncio.gather(*[rpc_call(rpc, mode=settings.HARD_MODE) for _ in range(10)])


if __name__ == "__main__":
    asyncio.run(main())