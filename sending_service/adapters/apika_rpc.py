import json

from aio_pika.patterns import RPC


class APikaRPC(RPC):
    CONTENT_TYPE = "application/json"

    def deserialize(self, data: str) -> dict:
        print(data)
        return json.loads(data)
