from fastapi import APIRouter, Depends, Body, Path, status
from typing import Annotated

from app.schemas.rooms import Room
from app import models


router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/{room_id}", status_code=status.HTTP_200_OK, response_model=Room)
async def get_specific_room(room_id: Annotated[str, Path(title="The id of specific room")]):
    """
        Getting specific room 
    """
    return models.Room.find_one({"id": room_id})


@router.patch("/{room_id}", status_code=status.HTTP_200_OK, response_model=Room)
async def update_room_info(room_id: Annotated[str, Path(title="The id of specific room")]):
    """
        Update room info
    """
    return ...


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Room)
async def create_new_room(room: Room):
    """
        Create new room
    """
    new_room = models.Room(name=room.name, columns=room.columns, rows=room.rows, places=room.places)
    await new_room.insert()
    return new_room


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Room])
async def get_all_rooms():
    """
        Getting all rooms saved in the database
    """
    return await models.Room.find_all().to_list()

