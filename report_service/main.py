import asyncio
import datetime

from aio_pika import connect_robust
from aio_pika.patterns import RPC
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pydantic import ValidationError
from redis.asyncio import Redis

from adapters.databases import async_mongo_client, Mongo, async_redis_client
from adapters.models import OutputMessage, InputMessage, Mode
from adapters.models.OutputMessage import Status
from services import CachingService, compile_reports
from settings import ReportSettings, report_settings


async_sheduler = AsyncIOScheduler(timezone='UTC')


async def get_phones_data(message: InputMessage,
                          mongo: Mongo = async_mongo_client,
                          redis: Redis = async_redis_client) -> str:
    recieved = datetime.datetime.now()

    cache = CachingService(mongo, redis)

    phone_data = None
    if message.mode.value == Mode.ACCURATE.value:
        phone_data = await compile_reports(mongo, message.phones)
    elif message.mode.value == Mode.FAST.value:
        phone_data = await cache.get_cached_phones_data(message.phones)

    if not phone_data:
        raise Exception(f"Message is wrong: {message}")
    try:
        out_message = OutputMessage(
            data=phone_data,
            status=Status.complete,
            task_received=recieved,
            total_duration=(datetime.datetime.now() - recieved).microseconds / 1000000,
            from_='report_service'
        )
    except ValidationError as e: #  Bug
        print(e)
    else:
        return out_message.model_dump_json(by_alias=True)


async def worker(index: int, settings: ReportSettings = report_settings):
    connection = await connect_robust(
        settings.rabbitmq_url,
        client_properties={"connection_name": f"callee{index}"},
    )

    channel = await connection.channel()

    rpc = await RPC.create(channel)
    await rpc.register("get_phones_data", get_phones_data, auto_delete=True)

    try:
        await asyncio.Future()
    finally:
        await connection.close()


async def main(settings: ReportSettings = report_settings,
               mongo: Mongo = async_mongo_client,
               redis: Redis = async_redis_client):

    await mongo.assure_indexes()

    cache = CachingService(mongo, redis)

    asyncio.get_running_loop().create_task(cache.phones_refresh_cache())
    async_sheduler.add_job(cache.phones_refresh_cache, 'interval',
                           minutes=settings.cache_refresh_interval_minutes)
    await asyncio.gather(*[worker(i) for i in range(10)])


if __name__ == "__main__":
    asyncio.run(main())
