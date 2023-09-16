from sqlalchemy import and_, or_, between
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.schemas.booking import Booking, BookingFromBase
from app import models


def create_booking(db: Session, booking: Booking):
    """
        Сreate new booking function with checking availability of the room
        If room already booked in that time, Error will be raised

        For example if i will use '|' to mark a interval we can imagine some intervals
        booking_in_base:       |___________________|

        booking_to_base: |__________________|

        booking_to_base               |_______________________|

        So, we can see that time to add can start before time_start in base and can finish before time_finish in base, so we should check it
    """
    db_room = db.query(models.Room).filter_by(id=booking.room_id).first()
    if not db_room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The room with this id doesn't exist")
    
    db_event = db.query(models.Event).filter_by(id=booking.event_id).first()
    if not db_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The event with this id doesn't exist")

    events_in_interval = db.query(models.Booking).filter(
        and_(
             or_(
                between(models.Booking.time_start, booking.time_start, booking.time_finish),
                between(models.Booking.time_finish, booking.time_start, booking.time_finish)
             ),
             models.Booking.room_id == db_room.id
    )).all()

    if events_in_interval:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The Room already have event it that time")
    
    new_booking = models.Booking(
        time_start=booking.time_start, 
        time_finish=booking.time_finish,
        additional_data=booking.additional_data
    )
    new_booking.event = db_event
    new_booking.room = db_room
    db.add(new_booking)
    db.commit()
    return new_booking


def get_all_booking_of_specific_room(db: Session, room_id: int | None = None, event_id: int | None = None):
    filter_properties = {}
    if room_id:
        filter_properties["room_id"] = room_id
    if event_id:
        filter_properties["event_id"] = room_id
    return db.query(models.Booking).filter_by(**filter_properties).all()
