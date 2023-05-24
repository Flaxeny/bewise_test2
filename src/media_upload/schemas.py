from pydantic import BaseModel
from pydantic.networks import AnyHttpUrl


class Url(BaseModel):
    url: AnyHttpUrl
