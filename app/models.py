import datetime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey


Base = declarative_base()


class Seat(Base):
    """
        Model that implement seat in the some room like theatre or cinema
    """
    __tablename__ = "seat"
    id = Column(Integer, primary_key=True)
    row = Column(Integer, nullable=False)
    column = Column(Integer, nullable=False)
    number = Column(Integer, nullable=False)
    booked = Column(Boolean, default=False)
    additional_data = Column(JSON)
    room_id = Column(Integer, ForeignKey("Room.id"))
    room = relationship("Room", back_populates="seats")
    
    def book(self):
        if self.booked:
            raise ValueError("The seat already booked")
        self.booked = True

    def unbook(self) -> None:
        if self.booked:
            self.booked = False


class Room(Base):
    """
        Model Room that implement room in the cinema or theatre
    """
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    seats = relationship("Seat", back_populates="room")
    events = relationship("Event", back_populates="events")

    async def generate_seats(self, rows, columns) -> list[Seat]:
        seats = []
        for row in range(1, rows + 1):
            for col in range(1, columns + 1):
                number_from_start = (row-1) * columns + col
                new_seat = Seat(column=col, row=row, number=number_from_start, room=self)
                seats.append(new_seat)
        return seats
    
    async def fill_room_by_seats(self, seats: list[Seat]) -> None:
        self.seats = seats
        # TODO: SAVE DATA TO DB


class Event(Base):
    """
        Model that implement specific Event like some perfomance or film
    """
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    time_start = Column(DateTime)
    time_finish = Column(DateTime)
    additional_data = Column(JSON)
    room_id = Column(Integer, ForeignKey("Room.id"))
    room = relationship("Room", back_populates="events")

    def __init__(self) -> None:
        """
            #TODO: MAKE CHECK IF TIME IS NOT BOOKED
        """
        pass