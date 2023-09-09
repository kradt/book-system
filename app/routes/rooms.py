from fastapi import APIRouter, Path, status, Depends, HTTPException
from typing import Annotated
from bson import ObjectId

from app.schemas.rooms import Room, RoomUpdate, RoomOutput
from app.schemas.seats import Seat, SeatCreate
from app.dependencies import get_room_by_id, get_seat_by_number
from app import models


router = APIRouter(tags=["Rooms"])


@router.get("/rooms/{room_id}/seats/{seat_number}/book", status_code=200, response_model=Seat)
async def book_a_seat(
        db_seat: Annotated[Seat, Depends(get_seat_by_number)],
        db_room: Annotated[models.Room, Depends(get_room_by_id)]):
    
    if db_seat.booked:
        raise HTTPException(400, "The seat already booked")
    db_seat.booked = True
    await db_room.save()
    return db_seat


@router.post("/rooms/{room_id}/seats", status_code=201, response_model=Seat)
def create_new_seat(
    db_room: Annotated[models.Room, Depends(get_room_by_id)],
    seat: SeatCreate):
    seats = db_room.seats
    new_seat = Seat()


@router.get("/rooms/{room_id}/seats/{seat_number}/", status_code=200, response_model=Seat)
def get_specific_seat(
        db_seat: Annotated[Seat, Depends(get_seat_by_number)]):
    return db_seat


@router.get("/rooms/{room_id}/seats/", status_code=200, response_model=list[Seat])
def get_seat_specific_room(db_room: Annotated[models.Room, Depends(get_room_by_id)]):
    return db_room.seats


@router.patch("/rooms/{room_id}", status_code=status.HTTP_200_OK, response_model=RoomOutput)
async def update_room_info(
    room: RoomUpdate,
    db_room: Annotated[models.Room, Depends(get_room_by_id)]):
    """
        Update room info
    """
    await db_room.set({"name": room.name})
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
async def create_new_room(room: Room):
    """
        Create new room
    """
    if await models.Room.find_one({"name": room.name}):
        raise HTTPException(status_code=404, detail="The room with same name already exist")
    new_room = models.Room(_id=ObjectId(), name=room.name, columns=room.columns, rows=room.rows, places=room.places)
    await new_room.insert()
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
