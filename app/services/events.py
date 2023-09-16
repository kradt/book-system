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
