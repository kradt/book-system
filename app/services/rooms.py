from app import models
from app.schemas.rooms import Room
from app.schemas.seats import Seat
from app.schemas.events import Event
from sqlalchemy import or_, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException


def create_room(db: Session, room: Room, autogenerate: bool = False, columns: int = 0, rows: int = 0):
    """
        Function createing new room and saving it into the database
    """
    try:
        new_room = models.Room(name=room.name)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="The room with the same name alreadt exist")
    
    if autogenerate:
        seats = new_room.generate_seats(columns=columns, rows=rows)
        db.add_all(seats)
    else:
        seats = [models.Seat(**seat.dict()) for seat in room.seats if seat] if room.seats else []
        db.add_all(seats)
    new_room.seats = seats
    try:
        db.add(new_room)
        db.commit()
    except:
        db.rollback()
    return new_room


def update_room(db: Session, db_room: models.Room, room: Room):
    if room.name:
        db_room.name = room.name
    if room.seats:
        [db.delete(seat) for seat in db_room.seats]
        db_room.seats = [models.Seat(**seat.dict(), room=db_room) for seat in room.seats]
    try:
        db.add(db_room)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="The room with the same name alreadt exist")
    return db_room


def update_seat(db, db_seat, seat: Seat):
    if seat.booked:
        try:
            if seat.booked == True: db_seat.book()
            elif seat.booked == False: db_seat.unbook()
        except ValueError:
            raise HTTPException(400, "The seat already booked")
    if seat.additional_data:
        db_seat.additional_data = seat.additional_data
    try:
        db.add(db_seat)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)
    return db_seat


def create_event(db, db_room, event: Event):
    """
        Function creating new event with checking available of the room
        IF room already booked in that time, Error will be raised
    """

    events_in_interval = db.query(models.Event).filter(
             or_(
                 and_(
                     models.Event.time_start <= event.time_start,
                     models.Event.time_finish >= event.time_finish
                 ),
                 and_(
                     models.Event.time_start >= event.time_start,
                     models.Event.time_finish <= event.time_finish
             ),
             models.Event.rooms.contains(db_room))
         ).all()

    if events_in_interval:
        raise HTTPException(status_code=400, detail="The Room already have event it that time")
    
    new_event = models.Event(
        title=event.title, 
        time_start=event.time_start, 
        time_finish=event.time_finish, 
        additional_data=event.additional_data)
    new_event.room = db_room
    try:
        db.add(new_event)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="The event with the same name already exist")
    return new_event