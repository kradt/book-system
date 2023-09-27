from fastapi import APIRouter, Depends, status, Query
from typing import Annotated
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_seat_by_number, get_seats
from app.services import seats as seat_service
from app.schemas.seats import Seat, SeatCreate
from app.schemas.rooms import Room




router = APIRouter(tags=["Seats"])


@router.patch("/rooms/{room_id}/seats/{seat_number}/", status_code=status.HTTP_200_OK, response_model=Seat)
async def update_seat_data(
        db: Annotated[Session, Depends(get_db)],
        db_seat: Annotated[Seat | None, Depends(get_seats)],
        seat: SeatCreate):
    """
        Update specific seat
        You can update additional data and booking status of seat
        If you want to change other data you should use patch method of Room to change all seats
    """
    return seat_service.update_seat(db, db_seat, seat)


@router.get("/rooms/{room_id}/seats/", status_code=status.HTTP_200_OK, response_model=list[Seat] | Seat)
def get_specific_seat(
        seats: Annotated[Seat | None, Depends(get_seats)]):
    """
        Get all seats specific room
    """
    return seats
