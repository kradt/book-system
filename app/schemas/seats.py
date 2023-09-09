from pydantic import BaseModel


class SeatCreate(BaseModel):
    """
        :booked: if seat booked set to True
        :additional_data: You can use it to pass some additional info like price or something else
    """
    booked: bool = False
    additional_data: dict | None = None

    class Config:
        from_orm = True


class Seat(SeatCreate):
    """
        :param column: number of column in columns
        :param row: number of row in rows
        :param number: seat number
        
    """
    column: int
    row: int
    number: int