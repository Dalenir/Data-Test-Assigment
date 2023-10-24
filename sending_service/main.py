import asyncio
import datetime
import json
import uuid
from typing import MutableMapping

from aio_pika import Message, connect, connect_robust
from aio_pika.abc import (
    AbstractChannel, AbstractConnection, AbstractIncomingMessage, AbstractQueue,
)
from aio_pika.patterns import RPC

from adapters.apika_rpc import APikaRPC
from models import ServiceMessage
from models.Message import Mode
from settings import SendSettings, send_settings

import random


def random_phones() -> list[int]:
    return [random.randint(0, 200) for _ in range(10)]


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
        for i in range(100):
            try:
                print(await rpc.proxy.get_phones_data(message=ServiceMessage(
                phones=random_phones(), mode=random.choice([Mode.ACCURATE, Mode.FAST])))
                  )
            except TypeError as e:
                print(e)


if __name__ == "__main__":
    asyncio.run(main())