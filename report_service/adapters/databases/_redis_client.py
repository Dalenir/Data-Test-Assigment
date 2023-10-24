from redis.asyncio.client import Redis

from settings import report_settings

async_redis_client = Redis(
    host=report_settings.REDIS_HOST,
    port=report_settings.REDIS_PORT,
    password=report_settings.REDIS_PASS,
    decode_responses=True,
    db=1
)
