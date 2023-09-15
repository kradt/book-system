from fastapi import HTTPException, Depends, Path, status
from sqlalchemy.orm import Session
from typing import Annotated 

from app import models, SessionLocal


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_room_by_id(
        db: Annotated[Session, Depends(get_db)],
        room_id: str) -> models.Room:
    """
        Depends that useing for getting specific room
    """
    room = db.query(models.Room).filter_by(id=room_id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no such room")
    return room


def get_seat_by_number(
        db: Annotated[Session, Depends(get_db)],
        db_room: Annotated[models.Room, Depends(get_room_by_id)], 
        seat_number: Annotated[int, Path(title="Number of seat in the room")]) -> models.Seat:
    """
        Depends that using for getting specific seat
    """
    seat = db.query(models.Seat).filter_by(room_id=db_room.id, number=seat_number).first()
    if not seat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no such seat")
    return seat


def get_event_by_id(
        db: Annotated[Session, Depends(get_db)],
        event_id: str) -> models.Event:
    """
        Depends that using for getting event by id
    """
    event = db.query(models.Event).filter_by(id=event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no such event")
    return event
