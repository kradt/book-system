import datetime
from pydantic import BaseModel

from .rooms import Room
from .events import Event


class BaseBooking(BaseModel):
    time_start: datetime.datetime | None
    time_finish: datetime.datetime | None
    additional_data: dict | None

    class Config:
        orm_mode = True


class BookingCreate(BaseBooking):
    room_id: int
    event_id: int


class Booking(BaseBooking):
    room: Room
    event: Event


class BookingFromBase(BookingCreate):
    id: int
