from enum import Enum

from pydantic import Field

from ._model import Model


class Status(Enum):
    complete = "Complete"
    failed = "Failed"


class Answer(Model):
    correlation_id: str
    status: Status
    task_received: str
    from_: str = Field(serialization_alias='from'),
    to: str
    data: list[OutputData]              # Already a json string
    total_duration: float
