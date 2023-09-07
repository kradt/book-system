from fastapi import APIRouter, Depends, Body, Path, status
from typing import Annotated

from app.schemas.rooms import Room


router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/{room_id}", status_code=status.HTTP_200_OK, response_model=Room)
def get_specific_room(room_id: Annotated[str, Path(title="The id of specific room")]):
    """
        Getting specific room 
    """
    return ...


@router.patch("/{room_id}", status_code=status.HTTP_200_OK, response_model=Room)
def update_room_info(room_id: Annotated[str, Path(title="The id of specific room")]):
    """
        Update room info
    """
    return ...


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Room)
def create_new_room(room: Room):
    """
        Create new room
    """
    return ...


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Room])
def get_all_rooms():
    """
        Getting all rooms saved in the database
    """
    return ...
