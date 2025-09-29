import uuid
from pydantic import BaseModel, validator, condecimal
from datetime import datetime
from typing import List


class Stop(BaseModel):
    city_id: uuid.UUID
    time: datetime
    longitude: float | None = None
    latitude: float | None = None


class TripBase(BaseModel):
    name: str
    price: condecimal(gt=0)
    bus_id: uuid.UUID
    route: List[Stop]


class TripCreate(TripBase):
    @validator("route")
    def validate_route(cls, value: List[Stop]):
        if len(value) < 2:
            raise ValueError("Route must have at least 2 stops")
        times = [stop.time for stop in value]
        if times != sorted(times):
            raise ValueError("Route must be in chronological order")
        return value


class TripUpdate(BaseModel):
    name: str | None = None
    price: condecimal(gt=0) | None = None
    route: List[Stop] | None = None

    @validator("route")
    def validate_route(cls, value: List[Stop]):
        if value and len(value) < 2:
            raise ValueError("Route must have at least 2 stops")
        if value:
            times = [stop.time for stop in value]
            if times != sorted(times):
                raise ValueError("Route must be in chronological order")
        return value


class TripRead(TripBase):
    id: uuid.UUID
    seats_left: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
