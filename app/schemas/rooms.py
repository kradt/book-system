from pydantic import BaseModel, Field
from bson import ObjectId

from .seats import Seat
from app.tools import PyObjectId


class RoomUpdate(BaseModel):
    """
        :param name: Name of room if it has
    """
    name: str | None = None

    class Config:
        orm_mode = True


class Room(RoomUpdate):
    """
        :param name: Name of room if it has
        :param columns: count of columns in the room
        :param rows: count of rows in the room
        :param places: all places that generated by number of column and rows
    """
    columns: int = 10
    rows: int = 5
    seats: list[Seat] | None = None


class RoomOutput(Room):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
