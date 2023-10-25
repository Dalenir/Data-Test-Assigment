from datetime import datetime
from enum import Enum

from pydantic import Field, field_validator

from ._model import Model
from .OutputData import OutputData


class Status(Enum):
    complete = "Complete"
    failed = "Failed"




class OutputMessage(Model):
    status: Status
    task_received: str | datetime
    from_: str = Field(serialization_alias='from'),
    to: str = "client"
    data: list[OutputData]              # Already a json string
    total_duration: float

    @field_validator('task_received')
    @classmethod
    def datetime_to_str(cls, dt: datetime | str) -> str:
        if isinstance(dt, str):
            return dt
        return dt.strftime("%Y-%m-%d %H:%M:%S.%f")
