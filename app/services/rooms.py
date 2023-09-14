from app import models
from app.schemas.rooms import Room
from app.schemas.seats import Seat
from app.schemas.events import Event
from sqlalchemy import or_, and_, between
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException


def create_room(db: Session, room: Room, autogenerate: bool = False, columns: int = 0, rows: int = 0):
    """
        Function createing new room and saving it into the database
    """
    if autogenerate:
        seats = new_room.generate_seats(columns=columns, rows=rows)
    else:
        seats = [models.Seat(**seat.dict()) for seat in room.seats if seat] if room.seats else []
    events = [models.Event(**event.dict()) for event in room.events] if room.events else []
    try:
        new_room = models.Room(name=room.name, seats=seats, events=events)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="The room with the same name alreadt exist")
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

        For example if i will use '|' for mark a interval we can imagine some intervals
        event_in_base:       |                  |
        event_to_base: |                   |
        event_to_base               |                 |
        
        So, we can see that time to add can start before start time and base and can finish before time finish in base, so we should check it
    """
    events_in_interval = db.query(models.Event).filter(
        and_(
             or_(
                between(models.Event.time_start, event.time_start, event.time_finish),
                between(models.Event.time_finish, event.time_start, event.time_finish)
             ),
             models.Event.rooms.contains(db_room)
    )).all()

    if events_in_interval:
        raise HTTPException(status_code=400, detail="The Room already have event it that time")
    
    new_event = models.Event(
        title=event.title, 
        time_start=event.time_start, 
        time_finish=event.time_finish, 
        additional_data=event.additional_data)
    
    new_event.rooms.append(db_room)
    try:
        db.add(new_event)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="The event with the same name already exist")
    return new_event
