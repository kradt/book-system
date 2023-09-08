from pydantic import BaseModel


class Place(BaseModel):
    """
        :param column: number of column in columns
        :param row: number of row in rows
        :booked: if place booked set to True
        :additional_data: You can use it to pass some additional info like price of something else
        
    """
    column: int
    row: int
    number: int
    booked: bool = False
    additional_data: dict | None = None


    class Config:
        from_orm = True