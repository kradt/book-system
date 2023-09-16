from pydantic import BaseModel


class Event(BaseModel):
    """
        :param time_start: datetime start specific event in the specific room
        :param additional_data: You can put on here everything what you want
    """
    title: str
    additional_data: dict | None = None

    class Config:
        orm_mode = True


class EventFromBase(Event):
    id: int
