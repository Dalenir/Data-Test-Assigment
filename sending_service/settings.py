from pydantic import computed_field
from pydantic_settings import BaseSettings

from models import Mode


class SendSettings(BaseSettings):
    RABBMQ_HOST: str
    RABBMQ_PORT: int
    RABBMQ_NAME: str = 'guest'
    RABBMQ_PASS: str = 'guest'

    HARD_MODE: Mode | None = None

    @computed_field
    @property
    def rabbitmq_url(self) -> str:
        return f"amqp://{self.RABBMQ_NAME}:{self.RABBMQ_PASS}@{self.RABBMQ_HOST}:{self.RABBMQ_PORT}"

send_settings = SendSettings()
