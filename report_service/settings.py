from pydantic import computed_field, Field
from pydantic_settings import BaseSettings


class ReportSettings(BaseSettings):

    cache_refresh_interval_minutes: int = Field(alias='REFRESH_INTERVAL_MINUTES', default=10)
    
    RABBMQ_HOST: str
    RABBMQ_PORT: int
    RABBMQ_NAME: str = 'guest'
    RABBMQ_PASS: str = 'guest'
    
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASS: str

    MONGO_NAME: str = Field(alias='MONGO_INITDB_ROOT_USERNAME')
    MONGO_PASS: str = Field(alias='MONGO_INITDB_ROOT_PASSWORD')
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_TSDB: str = 'test_db'
    MONGO_TCOL: str = 'test_coll'

    @computed_field
    @property
    def rabbitmq_url(self) -> str:
        return f"amqp://{self.RABBMQ_NAME}:{self.RABBMQ_PASS}@{self.RABBMQ_HOST}:{self.RABBMQ_PORT}"

report_settings = ReportSettings()
