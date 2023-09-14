from fastapi import APIRouter, status, Depends, HTTPException, Query
from typing import Annotated
from sqlalchemy.orm import Session

from app.schemas.rooms import Room, Seat
from app.schemas.seats import SeatCreate, Seat
from app.schemas.events import Event
from app.dependencies import get_room_by_id, get_seat_by_number, get_event_by_id, get_db
from app.services import rooms as room_service
from app import models


router = APIRouter()


@router.delete("/events/{event_id}/", tags=["Events"], status_code=204)
async def delete_event_by_id(
    db: Annotated[Session, Depends(get_db)],
    event: Annotated[Event, Depends(get_event_by_id)]):
    """
        Deleting specific event using it id
    """
    db.delete(event)
    db.commit()


@router.post("/rooms/{room_id}/events/", tags=["Events"], status_code=201, response_model=Event)
async def create_event(
        db: Annotated[Session, Depends(get_db)],
        db_room: Annotated[models.Room, Depends(get_room_by_id)],
        event: Event):
    """
        Create new event
    """
    new_event = room_service.create_event(db, db_room, event)
    return new_event


@router.get("/events/{event_id}/", tags=["Events"], status_code=200, response_model=Event | None)
def get_specific_event_by_id(event: Annotated[Event, Depends(get_event_by_id)]):
    """
        Get specific event using it id
    """
    return event


@router.get("/rooms/{room_id}/events/", tags=["Events"], status_code=200, response_model=list[Event] | None)
def get_all_event(db_room: Annotated[models.Room, Depends(get_room_by_id)]):
    """
        Get all events specific room
    """
    return db_room.events


@router.patch("/rooms/{room_id}/seats/{seat_number}/", tags=["Seats"], status_code=200, response_model=Seat)
async def update_seat_data(
        db: Annotated[Session, Depends(get_db)],
        db_seat: Annotated[Seat, Depends(get_seat_by_number)],
        seat: SeatCreate):
    """
        Update specific seat
        You can update additional data and booking status of seat
        If you want to change other data you should use patch method of room to change all seats
    """
    room_service.update_seat(db, db_seat, seat)
    return db_seat


@router.get("/rooms/{room_id}/seats/{seat_number}/", tags=["Seats"], status_code=200, response_model=Seat)
def get_specific_seat(
        db_seat: Annotated[Seat, Depends(get_seat_by_number)]):
    """
        Get specific Seat by seat number
    """
    return db_seat


@router.get("/rooms/{room_id}/seats/", tags=["Seats"], status_code=200, response_model=list[Seat])
def get_specific_seat(
        db_room: Annotated[Seat, Depends(get_room_by_id)]):
    """
        Get all seats specific room
    """
    return db_room.seats


@router.patch("/rooms/{room_id}/", tags=["Rooms"], status_code=status.HTTP_200_OK, response_model=Room)
async def update_room_info(
        db: Annotated[Session, Depends(get_db)],
        room: Room,
        db_room: Annotated[models.Room, Depends(get_room_by_id)]):
    """
        Update room info
    """
    room_service.update_room(db, db_room, room)
    return db_room


@router.delete("/rooms/{room_id}/", tags=["Rooms"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
        db: Annotated[Session, Depends(get_db)],
        db_room: Annotated[models.Room, Depends(get_room_by_id)]):
    """
        Remove room from base
    """
    db.delete(db_room)
    db.commit()


@router.post("/rooms/", tags=["Rooms"], status_code=status.HTTP_201_CREATED, response_model=Room)
async def create_new_room(
        db: Annotated[Session, Depends(get_db)],
        room: Room,
        autogenerate: Annotated[bool | None, Query(title="If True the seats will be generated before creating")] = False,
        columns: Annotated[int | None, Query(title="Amount of columns in the room")] = None,
        rows: Annotated[int | None, Query(title="Amount of rows in the room")] = None):
    """
        Create new room
    """
    if autogenerate and (not columns or not rows):
        raise HTTPException(status_code=400, detail="For using autogenerating you have to pass count of columns and rows")
    new_room = room_service.create_room(db, room, autogenerate, columns, rows)
    return new_room


@router.get("/rooms/{room_id}/", tags=["Rooms"], status_code=status.HTTP_200_OK, response_model=Room)
async def get_specific_room(db_room: Annotated[models.Room, Depends(get_room_by_id)]):
    """
        Getting specific room 
    """
    return db_room


@router.get("/rooms/", tags=["Rooms"], status_code=status.HTTP_200_OK, response_model=list[Room])
async def get_all_rooms(
        db: Annotated[Session, Depends(get_db)]):
    """
        Getting all rooms saved in the database
    """
    return db.query(models.Room).all()
