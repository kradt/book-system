import datetime
from pydantic import BaseModel
from app.schemas.rooms import Room


class EventCreate(BaseModel):
    """
        :param title: Title of event
        :param time_start: datetime start specific event in the specific room
        :param time_finish: datetime finish specific event in the specific room
        :param additional_data: You can put on here everything what you want
    """
    title: str
    time_start: datetime.datetime
    time_finish: datetime.datetime
    additional_data: dict


class Event(EventCreate):
    """
        :param room: Link for specific room where will be going current event
    """
    room: Room