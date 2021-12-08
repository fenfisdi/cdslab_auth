from datetime import datetime, date
from json import JSONEncoder as JSON
from typing import Any

from ujson import loads


class JSONEncoder(JSON):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime) or isinstance(o, date):
            return o.isoformat()


def encode_request(data: dict):
    raw = JSONEncoder().encode(data)
    return loads(raw)
