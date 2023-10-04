from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app import models
from app.schemas.rooms import Room


def create_room(db: Session, room: Room, autogenerate: bool = False, columns: int = 0, rows: int = 0) -> models.Room:
    """
        Room create function

        :param db: database session
        :param room: room from request body converted to pydantic model object
        :param autogenerate: if true the seats will be generated automatically
        :param columns: necessary count of columns of seats that will be generated
        :param rows: necessary count of rows of seats that will be generated
    """
    new_room = models.Room(name=room.name, additional_data=room.additional_data)
    
    if autogenerate:
        seats = new_room.generate_seats(columns=columns, rows=rows)
    else:
        seats = [models.Seat(**seat.dict()) for seat in room.seats if seat] if room.seats else []

    new_room.seats = seats
    try:
        db.add(new_room)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The room with the same name alreadt exist")
    return new_room


def update_room(db: Session, db_room: models.Room, room: Room) -> models.Room:
    """
        Room update function
        
        :param db: database session
        :param db_room: room from database
        :param room: room from request body converted to pydantic model object
    """
    if room.name:
        db_room.name = room.name
    if room.seats:
        [db.delete(seat) for seat in db_room.seats]
        db_room.seats = [models.Seat(**seat.dict(), room=db_room) for seat in room.seats]
    if room.additional_data:
        db_room.additional_data = room.additional_data
    try:
        db.add(db_room)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The room with the same name alreadt exist")
    return db_room
