from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_room_by_id, get_seat_by_number
from app.services import seats as seat_service
from app.schemas.seats import Seat, SeatCreate


router = APIRouter(tags=["Seats"])


@router.patch("/rooms/{room_id}/seats/{seat_number}/", status_code=status.HTTP_200_OK, response_model=Seat)
async def update_seat_data(
        db: Annotated[Session, Depends(get_db)],
        db_seat: Annotated[Seat, Depends(get_seat_by_number)],
        seat: SeatCreate):
    """
        Update specific seat
        You can update additional data and booking status of seat
        If you want to change other data you should use patch method of Room to change all seats
    """
    db_seat = seat_service.update_seat(db, db_seat, seat)
    return db_seat


@router.get("/rooms/{room_id}/seats/{seat_number}/", status_code=status.HTTP_200_OK, response_model=Seat)
def get_specific_seat(
        db_seat: Annotated[Seat, Depends(get_seat_by_number)]):
    """
        Get specific Seat by seat number
    """
    return db_seat


@router.get("/rooms/{room_id}/seats/", status_code=status.HTTP_200_OK, response_model=list[Seat])
def get_specific_seat(
        db_room: Annotated[Seat, Depends(get_room_by_id)]):
    """
        Get all seats specific room
    """
    return db_room.seats
