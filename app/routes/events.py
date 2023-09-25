from fastapi import APIRouter, Depends, status, Query
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


@router.get("/events/", status_code=status.HTTP_200_OK, response_model=list[EventFromBase] | None)
def get_all_events(
        db: Annotated[Session, Depends(get_db)],
        id: Annotated[int | None, Query(None, title="Event id")] = None,
        name: Annotated[str | None, Query(None, title="Event name")] = None):
    """
        Get All Events Function
    """
    filters = {k: v for k, v in {"id": id, "name": name}.items() if v}
    events = db.query(models.Event).filter_by(**filters).all()
    return events[0] if len(events) == 1 else events
