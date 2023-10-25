from pydantic import Field
from ._model import Model

class DurationsGroups(Model):
    ten_sec: float = Field(alias='10_sec')
    ten_thirty_sec: float = Field(alias='10_30_sec')
    thirty_sec: float = Field(alias='30_sec')


class OutputData(Model):
    phone: int
    cnt_all_attempts: int
    cnt_att_dur: DurationsGroups
    min_price_att: float
    max_price_att: float
    avg_dur_att: float
    sum_price_att_over_15: float
