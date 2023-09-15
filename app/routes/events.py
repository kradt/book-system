from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_event_by_id, get_room_by_id
from app.services import events as event_service
from app.schemas.events import Event
from app import models


router = APIRouter(tags=["Events"])


@router.delete("/events/{event_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event_by_id(
    db: Annotated[Session, Depends(get_db)],
    event: Annotated[Event, Depends(get_event_by_id)]):
    """
        Deleting specific event using it id
    """
    db.delete(event)
    db.commit()


@router.post("/rooms/{room_id}/events/", status_code=status.HTTP_201_CREATED, response_model=Event)
async def create_event(
        db: Annotated[Session, Depends(get_db)],
        db_room: Annotated[models.Room, Depends(get_room_by_id)],
        event: Event):
    """
        Create new event
    """
    new_event = event_service.create_event(db, db_room, event)
    return new_event


@router.get("/events/{event_id}/", status_code=status.HTTP_200_OK, response_model=Event | None)
def get_specific_event_by_id(event: Annotated[Event, Depends(get_event_by_id)]):
    """
        Get specific event using it id
    """
    return event


@router.get("/rooms/{room_id}/events/", status_code=status.HTTP_200_OK, response_model=list[Event] | None)
def get_all_event(db_room: Annotated[models.Room, Depends(get_room_by_id)]):
    """
        Get all events specific room
    """
    return db_room.events
