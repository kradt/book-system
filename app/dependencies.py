from fastapi import Depends, Path, Query
from sqlalchemy.orm import Session
from typing import Annotated 

from app import models, SessionLocal
from app.utills import is_exist


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_room_by_id(
        db: Annotated[Session, Depends(get_db)],
        room_id: Annotated[int, Path(title="ID of room")]) -> models.Room:
    """
        Depends that useing for getting specific room
    """
    room = db.query(models.Room).filter_by(id=room_id).first()
    is_exist(room, detail="There is no such room")
    return room


def get_seat_by_number(
        db: Annotated[Session, Depends(get_db)],
        db_room: Annotated[models.Room, Depends(get_room_by_id)], 
        seat_number: Annotated[int, Path(title="Number of seat in the room")]) -> models.Seat:
    """
        Depends that using for getting specific seat
    """
    seat = db.query(models.Seat).filter_by(room_id=db_room.id, number=seat_number).first()
    is_exist(seat, detail="There is no such seat")
    return seat


def get_event_by_id(
        db: Annotated[Session, Depends(get_db)],
        event_id: Annotated[int, Path(title="ID of event")]) -> models.Event:
    """
        Depends that using for getting event by id
    """
    event = db.query(models.Event).filter_by(id=event_id).first()
    is_exist(event, detail="There is no such event")
    return event


def get_booking_by_id(
        db: Annotated[Session, Depends(get_db)],
        booking_id: Annotated[int, Path(title="ID of booking")]) -> models.Booking:
    """
        Depends that using for getting booking by id
    """
    booking = db.query(models.Booking).filter_by(id=booking_id).first()
    is_exist(booking, detail="There is no such booking")
    return booking


def get_seats(
        db: Annotated[Session, Depends(get_db)],
        db_room: Annotated[models.Room, Depends(get_room_by_id)], 
        number: Annotated[int | None, Query(title="Number of seat")] = None,
        booked: Annotated[bool | None, Query(title="Booking of seat")] = None):
    filters = {key: value for key, value in {"number": number, "booked": booked} if value}
    seats = db.query(models.Seat).filter_by(**filters).all()
    return seats[0] if len(seats) == 1 else seats