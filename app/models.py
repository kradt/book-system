from beanie import Document, Indexed, init_beanie
from app.schemas.rooms import Seat
from app.tools import PyObjectId


class Room(Document):
    id: PyObjectId
    name: str | None = None
    columns: int
    rows: int
    seats: list[Seat] | None = None

    def __init__(
            self,
            *args,
            columns: int,
            rows: int,
            name: str | None = None,
            seats: list[Seat] | None = None,
            **kwargs):
        
        if seats is None:
            seats = []
            for row in range(1, rows + 1):
                for col in range(1, columns + 1):
                    number_from_start = (row-1) * columns + col
                    new_seat = Seat(column=col, row=row, number=number_from_start)
                    seats.append(new_seat)

        super().__init__(*args, name=name, columns=columns, rows=rows, seats=seats, **kwargs)

