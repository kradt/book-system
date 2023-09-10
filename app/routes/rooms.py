from fastapi import APIRouter, Path, status, Depends, HTTPException, Query
from typing import Annotated
from bson import ObjectId

from app.schemas.rooms import Room, RoomOutput, Seat
from app.schemas.seats import SeatCreate, Seat
from app.schemas.events import Event, EventCreate
from app.dependencies import get_room_by_id, get_seat_by_number, get_event_by_id
from app import models


router = APIRouter(tags=["Rooms"])


@router.delete("/room/{room_id}/events/{event_id}/", status_code=204)
def delete_event_by_id(event: Annotated[Event, Depends(get_event_by_id)]):
    pass


@router.post("/room/{room_id}/events/", status_code=201, response_model=Event)
async def create_event(
        db_room: Annotated[models.Room, Depends(get_room_by_id)],
        event: EventCreate):
    if await models.Event.time_is_booked(db_room, event.time_start, event.time_finish):
        raise HTTPException(status_code=400, detail="The Room already have event it that time")
    
    new_event = models.Event(
        _id=ObjectId(),
        title=event.title, 
        time_start=event.time_start, 
        time_finish=event.time_finish, 
        additional_data=event.additional_data, 
        room=db_room)
    
    await new_event.create()
    if db_room.events:
        db_room.events.append(new_event)
    else:
        db_room.events = [new_event]
    await db_room.save()
    return new_event


@router.get("room/{room_id}/events/{event_id}/", status_code=200, response_model=Event)
def get_specific_event_by_id(event: Annotated[Event, Depends(get_event_by_id)]):
    pass


@router.get("/room/{room_id}/events/{event_id}/", status_code=200, response_model=list[Event])
def get_all_event():
    pass


@router.patch("/rooms/{room_id}/seats/{seat_number}/", status_code=200, response_model=Seat)
async def update_seat_data(
        db_seat: Annotated[Seat, Depends(get_seat_by_number)],
        seat: SeatCreate):
    """
        Update specific seat
        You can update additional data and booking status of seat
        If you want to change other data you should use patch method of room to change all seats
    """
    try:
        if seat.booked == True: db_seat.book()
        elif seat.booked == False: db_seat.unbook()
    except ValueError:
        raise HTTPException(400, "The seat already booked")
    db_seat.additional_data = seat.additional_data
    await db_seat.save()
    return db_seat


@router.get("/rooms/{room_id}/seats/{seat_number}/", status_code=200, response_model=Seat)
def get_specific_seat(
        db_seat: Annotated[Seat, Depends(get_seat_by_number)]):
    """
        Get specific Seat by seat number
    """
    return db_seat


@router.patch("/rooms/{room_id}", status_code=status.HTTP_200_OK, response_model=RoomOutput)
async def update_room_info(
        room: Room,
        db_room: Annotated[models.Room, Depends(get_room_by_id)]):
    """
        Update room info
    """
    if room.name:
        await db_room.set({"name": room.name})
    if room.seats:
        await db_room.set({"name": room.seats})
    await db_room.save()
    return db_room


@router.delete("/rooms/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
        db_room: Annotated[models.Room, Depends(get_room_by_id)]):
    """
        Remove room from base
    """
    await db_room.delete()
    return {"message": f"The room with id {db_room.id} was Succefuly delete"}


@router.post("/rooms/", status_code=status.HTTP_201_CREATED, response_model=Room)
async def create_new_room(
        room: Room,
        autogenerate: Annotated[bool | None, Query(title="If True the seats will be generated before creating")] = None,
        columns: Annotated[int | None, Query(title="Amount of columns in the room")] = None,
        rows: Annotated[int | None, Query(title="Amount of rows in the room")] = None):
    """
        Create new room
    """
    if await models.Room.find_one({"name": room.name}):
        raise HTTPException(status_code=404, detail="The room with same name already exist")
    new_room = models.Room(_id=ObjectId(), name=room.name)
    await new_room.create()
    if autogenerate:
        seats = await new_room.generate_seats(columns=columns, rows=rows)
    else:
        seats = [models.Seat(**seat.dict()) for seat in room.seats]
    await new_room.fill_room_by_seats(seats)
    return new_room


@router.get("/rooms/{room_id}", status_code=status.HTTP_200_OK, response_model=RoomOutput)
async def get_specific_room(room_id: Annotated[str, Path(title="The id of specific room")]):
    """
        Getting specific room 
    """
    return await models.Room.get(room_id)


@router.get("/rooms/", status_code=status.HTTP_200_OK, response_model=list[RoomOutput])
async def get_all_rooms():
    """
        Getting all rooms saved in the database
    """
    return await models.Room.find_all().to_list()
