from fastapi import APIRouter, Depends, status, Query
from typing import Annotated
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_seats, get_seat_by_id
from app.services import seats as seat_service
from app.schemas.seats import Seat, SeatCreate, SeatFromBase


router = APIRouter(tags=["Seats"])


@router.patch("/seats/{seat_id}/", status_code=status.HTTP_200_OK, response_model=SeatFromBase)
async def update_seat_data(
        db: Annotated[Session, Depends(get_db)],
        db_seat: Annotated[Seat | None, Depends(get_seat_by_id)],
        seat: SeatCreate):
    """
        Update specific seat
        You can update additional data and booking status of seat
        If you want to change other data you should use patch method of Room to change all seats
    """
    return seat_service.update_seat(db, db_seat, seat)


@router.get("/seats/{seat_id}/", status_code=status.HTTP_200_OK, response_model=SeatFromBase)
async def update_seat_data(
        db_seat: Annotated[Seat | None, Depends(get_seat_by_id)]):
    """
        Get specific seat by its it
    """
    return db_seat


@router.get("/rooms/{room_id}/seats/", status_code=status.HTTP_200_OK, response_model=list[SeatFromBase])
def get_specific_seat(
        seats: Annotated[Seat | None, Depends(get_seats)]):
    """
        Get all seats specific room
    """
    return seats
