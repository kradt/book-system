from fastapi import APIRouter, Depends, Body, Path, status
from typing import Annotated

from app.schemas.rooms import Room, RoomUpdate, RoomOutput
from app import models


router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/{room_id}", status_code=status.HTTP_200_OK, response_model=Room)
async def get_specific_room(room_id: Annotated[str, Path(title="The id of specific room")]):
    """
        Getting specific room 
    """
    return models.Room.find_one({"id": room_id})


@router.patch("/{room_id}", status_code=status.HTTP_200_OK, response_model=RoomOutput)
async def update_room_info(
    room_id: Annotated[str, Path(title="The id of specific room")],
    room: RoomUpdate):
    """
        Update room info
    """
    db_room = models.Room.find({"_id": room_id})
    if not db_room:
        pass
        # Raise Error

    db_room.name = room.name
    db_room.replace()

   
    return db_room


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Room)
async def create_new_room(room: Room):
    """
        Create new room
    """
    new_room = models.Room(name=room.name, columns=room.columns, rows=room.rows, places=room.places)
    await new_room.insert()
    return new_room


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[RoomOutput])
async def get_all_rooms():
    """
        Getting all rooms saved in the database
    """
    return await models.Room.find_all().to_list()

