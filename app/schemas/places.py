from pydantic import BaseModel


class Seat(BaseModel):
    """
        :param column: number of column in columns
        :param row: number of row in rows
        :booked: if seat booked set to True
        :additional_data: You can use it to pass some additional info like price or something else
        
    """
    column: int
    row: int
    number: int
    booked: bool = False
    additional_data: dict | None = None


    class Config:
        from_orm = True