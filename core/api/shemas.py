from pydantic import BaseModel


class PingResponseModel(BaseModel):
    result: bool
