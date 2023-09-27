from pydantic import BaseModel, Field


class SeatCreate(BaseModel):
    """
        :booked: if seat booked set to True
        :additional_data: You can use it to pass some additional info like price or something else
    """
    booked: bool = False
    additional_data: dict | None = None

    class Config:
        orm_mode = True


class Seat(SeatCreate):
    """
        :param column: number of column in columns
        :param row: number of row in rows
        :param number: seat number
    """
    column: int = Field(gt=0)
    row: int = Field(gt=0)
    number: int = Field(gt=0)

class SeatFromBase(Seat):
    id: int