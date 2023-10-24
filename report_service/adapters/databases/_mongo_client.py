from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from settings import report_settings


class Mongo:

    def __init__(self, host: str, port: str, username: str, password: str,
                 data_db_name: str, data_collection_name: str):
        self.client = AsyncIOMotorClient(host=host, port=port, username=username, password=password)
        self.data_collection: AsyncIOMotorCollection = self.client[data_db_name][data_collection_name]

    async def assure_indexes(self):
        await self.data_collection.create_index("phone")


def fresh_mongo_client():
    return Mongo(
        host=report_settings.MONGO_HOST,
        port=report_settings.MONGO_PORT,
        username=report_settings.MONGO_NAME,
        password=report_settings.MONGO_PASS,
        data_db_name=report_settings.MONGO_TSDB,
        data_collection_name=report_settings.MONGO_TCOL
    )

async_mongo_client = fresh_mongo_client()
