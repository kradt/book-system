from fastapi import APIRouter, Path, status, Depends
from typing import Annotated

from app.schemas.rooms import Room, RoomUpdate, RoomOutput
from app.dependencies import get_room
from app import models


router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/{room_id}", status_code=status.HTTP_200_OK, response_model=RoomOutput)
async def get_specific_room(room_id: Annotated[str, Path(title="The id of specific room")]):
    """
        Getting specific room 
    """
    return await models.Room.get(room_id)


@router.patch("/{room_id}", status_code=status.HTTP_200_OK, response_model=RoomOutput)
async def update_room_info(
    room_id: Annotated[str, Path(title="The id of specific room")],
    room: RoomUpdate,
    db_room: Annotated[models.Room, Depends(get_room)]):
    """
        Update room info
    """
    await db_room.set({"name": room.name})
    return db_room


@router.delete("/{room_id}", status_code=204)
async def delete_room(
        room_id: Annotated[str, Path(title="The id of specific room")],
        db_room: Annotated[models.Room, Depends(get_room)]):
    """
        Remove room from base
    """
    await db_room.delete()
    return {"message": f"The room with id {room_id} was Succefuly delete"}


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
