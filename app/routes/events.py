from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_event_by_id
from app.services import events as event_service
from app.schemas.events import Event, EventFromBase
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


@router.post("/events/", status_code=status.HTTP_201_CREATED, response_model=EventFromBase)
async def create_event(
        db: Annotated[Session, Depends(get_db)],
        event: Event):
    """
        Create new event
    """
    return event_service.create_event(db, event)


@router.get("/events/{event_id}/", status_code=status.HTTP_200_OK, response_model=EventFromBase | None)
def get_specific_event_by_id(event: Annotated[Event, Depends(get_event_by_id)]):
    """
        Get specific event using it id
    """
    return event


@router.get("/events/", status_code=status.HTTP_200_OK, response_model=list[EventFromBase] | None)
def get_all_events(db: Annotated[Session, Depends(get_db)]):
    """
        Get All Events Function
    """
    return db.query(models.Event).all()
