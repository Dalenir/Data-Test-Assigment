import json

from redis.asyncio import Redis

from adapters.databases import Mongo
from adapters.models import OutputData
from ._compile_reports import compile_reports

class CachingService:
    mongo: Mongo
    redis: Redis

    def __init__(self, mongo: Mongo, redis: Redis):
        self.mongo = mongo
        self.redis = redis

    async def phones_refresh_cache(self):
        phones_data = await compile_reports(self.mongo)
        await self.redis.mset({phone.phone: phone.model_dump_json(by_alias=True) for phone in phones_data})

    async def get_cached_phones_data(self, phone_numbers: list[int]) -> list[OutputData]:
        red_list = await self.redis.mget([str(ph_numb) for ph_numb in phone_numbers])
        return [OutputData.model_validate_json(phone_data) for phone_data in red_list]
