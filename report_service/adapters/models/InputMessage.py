from enum import Enum
from ._model import Model


class Mode(Enum):
    FAST = 'fast'
    ACCURATE = 'accurate'

class InputMessage(Model):
    phones: list[int]
    mode: Mode
