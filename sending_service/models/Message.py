from enum import Enum

from ._model import Model


class Mode(Enum):
    FAST = 'fast'
    ACCURATE = 'accurate'

class ServiceMessage(Model):
    correlation_id: str | None = None
    phones: list[int]
    mode: Mode
