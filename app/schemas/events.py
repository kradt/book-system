import datetime
from pydantic import BaseModel



class Event(BaseModel):
    """
        :param title: Title of event
        :param time_start: datetime start specific event in the specific room
        :param time_finish: datetime finish specific event in the specific room
        :param additional_data: You can put on here everything what you want
    """
    title: str
    time_start: datetime.datetime
    time_finish: datetime.datetime
    additional_data: dict | None = None

    class Config:
        orm_mode = True
