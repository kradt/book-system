from sqlalchemy import and_, or_, between
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.schemas.events import Event
from app import models


def create_event(db: Session, db_room: models.Room, event: Event) -> models.Event:
    """
        Сreate new event function with checking availability of the room
        If room already booked in that time, Error will be raised

        For example if i will use '|' to mark a interval we can imagine some intervals
        event_in_base:       |___________________|

        event_to_base: |__________________|

        event_to_base               |_______________________|

        So, we can see that time to add can start before time_start in base and can finish before time_finish in base, so we should check it
    """
    events_in_interval = db.query(models.Event).filter(
        and_(
             or_(
                between(models.Event.time_start, event.time_start, event.time_finish),
                between(models.Event.time_finish, event.time_start, event.time_finish)
             ),
             models.Event.room == db_room
    )).all()

    if events_in_interval:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The Room already have event it that time")
    
    new_event = models.Event(
         title=event.title, 
         additional_data=event.additional_data
    )
    new_booking = models.Event(
        time_start=event.time_start, 
        time_finish=event.time_finish
    )
    new_event.performance = new_event
    new_event.room = db_room

    try:
        db.add(new_event)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The event with the same name already exist")
    return new_event
