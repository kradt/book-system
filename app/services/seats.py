from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.seats import Seat
from app import models


def update_seat(db: Session, db_seat: models.Seat, seat: Seat) -> models.Seat:
    """
        Seat update function

        :param db: database session
        :param db_seat: seat from database
        :param seat: seat from request_body converted to pydantic model object
    """
    if db_seat.booked and seat.booked:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The seat already booked")
    
    if seat.booked in [True, False]:
        db_seat.booked = seat.booked

    if seat.additional_data:
        db_seat.additional_data = seat.additional_data
    db.add(db_seat)
    db.commit()
    return db_seat
