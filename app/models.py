from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey


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


class Booking(Base):
    """
        Model that implement some booking using relation Room with Event and adding additional data like time start and time finish
    """
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True)
    time_start = Column(DateTime, nullable=False)
    time_finish = Column(DateTime, nullable=False)
    additional_data = Column(JSON)

    room_id = Column(Integer, ForeignKey("rooms.id"))
    event_id = Column(Integer, ForeignKey("events.id"))

    room = relationship("Room", back_populates="booking")
    event = relationship("Event", back_populates="booking")
    __mapper_args__ = {'confirm_deleted_rows': False}


class Room(Base):
    """
        Model Room that implement room in the cinema or theatre
    """
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    additional_data = Column(JSON)

    seats = relationship("Seat", back_populates="room", cascade="save-update, merge, delete, delete-orphan", order_by="Seat.number")
    booking = relationship("Booking", passive_deletes=True, back_populates="room", cascade="all, delete")
    __mapper_args__ = {'confirm_deleted_rows': False}

    def generate_seats(self, rows, columns) -> list[Seat]:
        seats = []
        for row in range(1, rows + 1):
            for col in range(1, columns + 1):
                number_from_start = (row-1) * columns + col
                new_seat = Seat(column=col, row=row, number=number_from_start, room=self)
                seats.append(new_seat)
        return seats


class Event(Base):
    """
        Model that implement specific Event like some Event or film
    """
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True)
    additional_data = Column(JSON)
    __mapper_args__ = {'confirm_deleted_rows': False}

    booking = relationship("Booking", passive_deletes=True, back_populates="event", cascade="all, delete")
