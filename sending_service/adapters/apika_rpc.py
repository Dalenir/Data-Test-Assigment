from aio_pika.patterns import RPC

import json


class APikaRPC(RPC):
    CONTENT_TYPE = "application/json"

    def deserialize(self, data: str) -> dict:
        print(data)
        return json.loads(data)
