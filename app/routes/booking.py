from fastapi import APIRouter, Depends, status, Query
from typing import Annotated
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_room_by_id, get_event_by_id
from app.services import booking as booking_service
from app.schemas.booking import Booking, BookingCreate
from app import models


router = APIRouter(tags=["Booking"])


@router.post("/booking", status_code=status.HTTP_201_CREATED, response_model=Booking)
def create_new_booking(
    db: Annotated[Session, Depends(get_db)],
    booking: BookingCreate):
    """
        Create new booking
    """
    return booking_service.create_booking(db, booking)


@router.get("/booking/", status_code=status.HTTP_200_OK, response_model=list[Booking] | None)
def get_all_event(
    db: Annotated[Session, Depends(get_db)],
    room_id: Annotated[int | None, Query(title="ID of room")] = None,
    event_id: Annotated[int | None, Query(title="ID of event")] = None):
    """
        Get all events specific room
    """
    return booking_service.get_all_booking_of_specific_room(db, room_id, event_id)
