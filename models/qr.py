from pydantic import BaseModel, AnyUrl
from typing import Any


class qr(BaseModel):
    qr_key: str
    qr_url: AnyUrl
    qr_img: Any
