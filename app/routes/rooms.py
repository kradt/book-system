from fastapi import APIRouter, Path, status, Depends, HTTPException, Query
from typing import Annotated
from bson import ObjectId
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.rooms import Room, Seat
from app.schemas.seats import SeatCreate, Seat
from app.schemas.events import Event
from app.dependencies import get_room_by_id, get_seat_by_number, get_event_by_id, get_session
from app import models


router = APIRouter()


@router.delete("/events/{event_id}/", tags=["Events"], status_code=204)
async def delete_event_by_id(event: Annotated[Event, Depends(get_event_by_id)]):
    """
        Deleting specific event using it id
    """
    await event.delete()


@router.post("/room/{room_id}/events/", tags=["Events"], status_code=201, response_model=Event)
async def create_event(
        db_room: Annotated[models.Room, Depends(get_room_by_id)],
        event: Event):
    """
        Create new event
    """
    if await models.Event.time_is_booked(db_room, event.time_start, event.time_finish):
        raise HTTPException(status_code=400, detail="The Room already have event it that time")
    
    new_event = models.Event(
        _id=ObjectId(),
        title=event.title, 
        time_start=event.time_start, 
        time_finish=event.time_finish, 
        additional_data=event.additional_data, 
        room=db_room)
    new_event.room = db_room
    await new_event.create()
    return new_event


@router.get("/events/{event_id}/", tags=["Events"], status_code=200, response_model=Event | None)
def get_specific_event_by_id(event: Annotated[Event, Depends(get_event_by_id)]):
    """
        Get specific event using it id
    """
    return event


@router.get("/room/{room_id}/events/", tags=["Events"], status_code=200, response_model=list[Event] | None)
def get_all_event(db_room: Annotated[models.Room, Depends(get_room_by_id)]):
    """
        Get all events specific room
    """
    return db_room.events


@router.patch("/rooms/{room_id}/seats/{seat_number}/", tags=["Seats"], status_code=200, response_model=Seat)
async def update_seat_data(
        db_seat: Annotated[Seat, Depends(get_seat_by_number)],
        seat: SeatCreate):
    """
        Update specific seat
        You can update additional data and booking status of seat
        If you want to change other data you should use patch method of room to change all seats
    """
    if seat.booked:
        try:
            if seat.booked == True: db_seat.book()
            elif seat.booked == False: db_seat.unbook()
        except ValueError:
            raise HTTPException(400, "The seat already booked")
    if seat.additional_data:
        db_seat.additional_data = seat.additional_data
    await db_seat.save()
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
        room: Room,
        db_room: Annotated[models.Room, Depends(get_room_by_id)]):
    """
        Update room info
    """
    if room.name:
        db_room.name = room.name
    if room.seats:
        db_room.seats = [models.Seat(**seat.dict(), room=db_room) for seat in room.seats]
    await db_room.save()
    return db_room


@router.delete("/rooms/{room_id}/", tags=["Rooms"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
        db_room: Annotated[models.Room, Depends(get_room_by_id)]):
    """
        Remove room from base
    """
    await db_room.delete()


@router.post("/rooms/", tags=["Rooms"], status_code=status.HTTP_201_CREATED, response_model=Room)
async def create_new_room(
        db: Annotated[AsyncSession, Depends(get_session)],
        room: Room,
        autogenerate: Annotated[bool | None, Query(title="If True the seats will be generated before creating")] = None,
        columns: Annotated[int | None, Query(title="Amount of columns in the room")] = None,
        rows: Annotated[int | None, Query(title="Amount of rows in the room")] = None):
    """
        Create new room
    """
    query = await db.execute(select(models.Room).where(models.Room.name == room.name))
    rooms = query.scalars().all()
    print("ROOMS", rooms)
    if rooms:
        raise HTTPException(status_code=404, detail="The room with same name already exist")
    try:
        new_room = models.Room(name=room.name)
    except Exception as e:
        print(e)
        
    # if autogenerate:
    #     seats = new_room.generate_seats(columns=columns, rows=rows)
    #     db.add_all(seats)
    # else:
    #     seats = [models.Seat(**seat.dict()) for seat in room.seats if seat] if room.seats else []
    #     db.add_all(seats)
    # await new_room.fill_room_by_seats(seats)
    try:
        db.add(new_room)
        await db.commit()
    except:
        await db.rollback()
    print(new_room)
    return new_room


@router.get("/rooms/{room_id}/", tags=["Rooms"], status_code=status.HTTP_200_OK, response_model=Room)
async def get_specific_room(room_id: Annotated[str, Path(title="The id of specific room")]):
    """
        Getting specific room 
    """
    return await models.Room.get(room_id)


@router.get("/rooms/", tags=["Rooms"], status_code=status.HTTP_200_OK, response_model=list[Room])
async def get_all_rooms():
    """
        Getting all rooms saved in the database
    """
    return await models.Room.find_all().to_list()
