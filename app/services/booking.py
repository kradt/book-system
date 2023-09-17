import datetime
from sqlalchemy import and_, or_, between
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.booking import Booking, BaseBooking
from app.utills import is_exist
from app import models


def is_time_booked(
        db: Session,
        time_start: datetime.datetime, 
        time_finish: datetime.datetime, 
        room_id: int) -> bool:
    """
        Return True if time have already booked in passed time
    """
    events_in_interval = db.query(models.Booking).filter(
        and_(
             or_(
                between(models.Booking.time_start, time_start, time_finish),
                between(models.Booking.time_finish, time_start, time_finish)
             ),
             models.Booking.room_id == room_id
    )).all()
    return bool(events_in_interval)


def create_booking(db: Session, booking: Booking) -> models.Booking:
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
    is_exist(db_room, detail="The room with this id doesn't exist")
    db_event = db.query(models.Event).filter_by(id=booking.event_id).first()
    is_exist(db_event, detail="The event with this id doesn't exist")

    if is_time_booked(db, time_start=booking.time_start, time_finish=booking.time_finish, room_id=db_room.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The Room has already had event it that time")
    
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


def get_all_booking_of_specific_room(
        db: Session,
        room_id: int | None = None, 
        event_id: int | None = None) -> list[models.Booking]:
    """
        Get all booking of specific room
    """
    filter_properties = {}
    if room_id:
        filter_properties["room_id"] = room_id
    if event_id:
        filter_properties["event_id"] = room_id
    return db.query(models.Booking).filter_by(**filter_properties).all()


def update_booking(db: Session, db_booking: models.Booking, booking: BaseBooking) -> models.Booking:
    """
        Update some room
    """
    if is_time_booked(db, time_start=booking.time_start, time_finish=booking.time_finish, room_id=db_booking.room.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The Room already have event it that time")
    
    if booking.time_start:
        db_booking.time_finish = booking.time_start
    if booking.time_finish:
        db_booking.time_finish = booking.time_finish
    if booking.additional_data:
        db_booking.additional_data = booking.additional_data
    db.add(db_booking)
    db.commit()
    return db_booking
