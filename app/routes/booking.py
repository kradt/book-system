from fastapi import APIRouter, Depends, status, Query
from typing import Annotated
from sqlalchemy.orm import Session

from app import models
from app.dependencies import get_db, get_booking_by_id
from app.services import booking as booking_service
from app.schemas.booking import BookingCreate, BookingFromBase, BaseBooking


router = APIRouter(tags=["Booking"])


@router.post("/booking/", status_code=status.HTTP_201_CREATED, response_model=BookingFromBase)
def create_new_booking(
        db: Annotated[Session, Depends(get_db)],
        booking: BookingCreate):
    """
        Create new booking
    """
    return booking_service.create_booking(db, booking)


@router.get("/booking/", status_code=status.HTTP_200_OK, response_model=list[BookingFromBase] | None)
def get_all_booking(
        db: Annotated[Session, Depends(get_db)],
        room_id: Annotated[int | None, Query(title="ID of room")] = None,
        event_id: Annotated[int | None, Query(title="ID of event")] = None):
    """
        Get all events specific room
    """
    return booking_service.get_all_booking_of_specific_room(db, room_id, event_id)


@router.patch("/booking/{booking_id}/", status_code=status.HTTP_200_OK, response_model=BookingFromBase)
def update_booking_by_id(
        db: Annotated[Session, Depends(get_db)],
        db_booking: Annotated[models.Booking, Depends(get_booking_by_id)],
        booking: BaseBooking):
    """
        Update specific booking
    """
    return booking_service.update_booking(db=db, db_booking=db_booking, booking=booking)


@router.delete("/booking/{booking_id}/", status_code=204)
def delete_booking(
        db: Annotated[Session, Depends(get_db)],
        db_booking: Annotated[models.Booking, Depends(get_booking_by_id)]):
    """
        Delete booking by id
    """
    db.delete(db_booking)
    db.commit()
