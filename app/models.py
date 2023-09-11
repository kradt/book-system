import datetime
from beanie import Document, Link, BackLink
from pydantic import Field
from beanie.odm.operators.find.comparison import GTE, LTE
from beanie.odm.operators.find.logical import Or, And
from app.tools import PyObjectId


class Seat(Document):
    """
        Model that implement seat in the some room like theatre or cinema
    """
    row: int
    column: int
    number: int 
    booked: bool = False
    additional_data: dict | None = None
    room: BackLink["Room"] = Field(original_field="seats")
    
    def book(self):
        if self.booked:
            raise ValueError("The seat already booked")
        self.booked = True

    def unbook(self) -> None:
        if self.booked:
            self.booked = False


class Room(Document):
    """
        Model Room that implement room in the cinema or theatre
    """
    id: PyObjectId
    name: str | None = None
    seats: list[Link[Seat]] | None = None
    events: list[Link["Event"]] | None = None

    async def generate_seats(self, rows, columns) -> list[Seat]:
        seats = []
        for row in range(1, rows + 1):
            for col in range(1, columns + 1):
                number_from_start = (row-1) * columns + col
                new_seat = Seat(column=col, row=row, number=number_from_start, room=self)
                await new_seat.create()
                seats.append(new_seat)
        return seats
    
    async def fill_room_by_seats(self, seats: list[Seat]) -> None:
        self.seats = seats
        await self.save()


class Event(Document):
    """
        Model that implement specific Event like some perfomance or film
    """
    id: PyObjectId
    title: str
    time_start: datetime.datetime
    time_finish: datetime.datetime
    additional_data: dict | None
    room: BackLink[Room] = Field(original_field="events")

    @classmethod
    async def time_is_booked(cls, room: Room, time_from: datetime.datetime, time_finish: datetime.timedelta) -> bool:
        events_in_interval = await Event.find(
            Or(
                And(
                    LTE(Event.time_start, time_from),
                    GTE(Event.time_finish, time_finish)
                ),
                And(
                    GTE(Event.time_start, time_from),
                    LTE(Event.time_finish, time_finish)
            ),
            Event.room.id == room.id)
        ).to_list()
        return events_in_interval
