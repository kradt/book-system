from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.schemas.events import Event
from app import models
    

def create_event(db: Session, event: Event) -> models.Event:
    """
        Create New Event Function
    """
    new_event = models.Event(
         title=event.title, 
         additional_data=event.additional_data
    )
    try:
        db.add(new_event)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The event with the same name already exist")
    return new_event


def update_event(db: Session, db_event: models.Event, event: Event) -> models.Event:
    """
        Event update function
        :param db: database session
        :param db_event: event from database
        :param event: event from request body converted to pydantic model object
    """
    if event.title:
        db_event.title = event.title
    if event.additional_data:
        db_event.additional_data = event.additional_data
    try:
        db.add(db_event)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The event with the same title already exist")
    return db_event