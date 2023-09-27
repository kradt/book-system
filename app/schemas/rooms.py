from pydantic import BaseModel

from app.schemas.seats import SeatFromBase, Seat


class BaseRoom(BaseModel):
    name: str | None = None


class Room(BaseRoom):
    """
        :param name: Name of room if it has
    """
    seats: list[SeatFromBase] | None = None
    
    class Config:
        orm_mode = True


class RoomCreate(BaseRoom):
    seats: list[Seat] | None = None


class RoomFromBase(Room):
    id: int
