from pydantic import BaseModel, Field


class Signal(BaseModel):
    source: str = Field(min_length=1)
    message: str = Field(min_length=1)


class OrderTriageRequest(BaseModel):
    order_id: str = Field(min_length=1)
    city: str = Field(min_length=1)
    signals: list[Signal] = Field(min_length=1)
