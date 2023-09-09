from beanie import Document, Link
from app.tools import PyObjectId


class Seat(Document):

    row: int
    column: int
    number: int 
    booked: bool = False
    additional_data: dict | None = None
    
    def book(self):
        if self.booked:
            raise ValueError("The seat already booked")
        self.booked = True

    def unbook(self) -> None:
        if self.booked:
            self.booked = False


class Room(Document):
    id: PyObjectId
    name: str | None = None
    seats: list[Link[Seat]] | None = None

    def generate_seats(self, rows, columns) -> list[Seat]:
        seats = []
        for row in range(1, rows + 1):
            for col in range(1, columns + 1):
                number_from_start = (row-1) * columns + col
                new_seat = Seat(column=col, row=row, number=number_from_start)
                seats.append(new_seat)
        return seats
    
    def fill_room_by_seats(self, seats: list[Seat]) -> None:
        self.seats = seats
