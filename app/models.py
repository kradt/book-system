from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey, Table


Base = declarative_base()


class Seat(Base):
    """
        Model that implement seat in the some room like theatre or cinema
    """
    __tablename__ = "seats"
    id = Column(Integer, primary_key=True)
    row = Column(Integer, nullable=False)
    column = Column(Integer, nullable=False)
    number = Column(Integer, nullable=False)
    booked = Column(Boolean, default=False)
    additional_data = Column(JSON)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete='CASCADE'), nullable=False)
    room = relationship("Room", back_populates="seats")
    __mapper_args__ = {'confirm_deleted_rows': False}


class Event(Base):
    __tablename__ = "events"

    room_id = Column(Integer, ForeignKey("rooms.id"))
    event_id = Column(Integer, ForeignKey("performances.id"))
    time_start = Column(DateTime, nullable=False)
    time_finish = Column(DateTime, nullable=False)
    room = relationship("Room", back_populates="events")
    performance = relationship("Performance", back_populates="rooms")


class Room(Base):
    """
        Model Room that implement room in the cinema or theatre
        so, about events field i have a discussion with myself about right way
        
        for example:
            We have film A and Room B
            Film A many times perform in the Room B
            so, question in how right save this data
            We add new Event to Room.events every time now,
            but when we add the same events but in different time it is not very good because in fact it is the same objects

        to solve it we can create association table with additional fields where we put time_start and time_finish of event
    """
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    seats = relationship("Seat", back_populates="room", cascade="save-update, merge, delete, delete-orphan")
    events = relationship("Event", back_populates="room", cascade="all, delete")

    def generate_seats(self, rows, columns) -> list[Seat]:
        seats = []
        for row in range(1, rows + 1):
            for col in range(1, columns + 1):
                number_from_start = (row-1) * columns + col
                new_seat = Seat(column=col, row=row, number=number_from_start, room=self)
                seats.append(new_seat)
        return seats


class Performance(Base):
    """
        Model that implement specific Event like some perfomance or film
    """
    __tablename__ = "performances"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True)
    time_start = Column(DateTime, nullable=False)
    time_finish = Column(DateTime, nullable=False)
    additional_data = Column(JSON)
    rooms = relationship("Event", back_populates="performance", cascade="all, delete")
