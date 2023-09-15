from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schemas.rooms import Room
from app.dependencies import (
    get_room_by_id,
    get_db
)
from app.services import rooms as room_service
from app import models


router = APIRouter(tags=["Rooms"])


@router.patch("/rooms/{room_id}/", status_code=status.HTTP_200_OK, response_model=Room)
async def update_room_info(
        db: Annotated[Session, Depends(get_db)],
        room: Room,
        db_room: Annotated[models.Room, Depends(get_room_by_id)]):
    """
        Update room info
    """
    room_service.update_room(db, db_room, room)
    return db_room


@router.delete("/rooms/{room_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
        db: Annotated[Session, Depends(get_db)],
        db_room: Annotated[models.Room, Depends(get_room_by_id)]):
    """
        Remove room from base
    """
    db.delete(db_room)
    db.commit()


@router.post("/rooms/", status_code=status.HTTP_201_CREATED, response_model=Room)
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="For using autogenerating you have to pass count of columns and rows")
    new_room = room_service.create_room(db, room, autogenerate, columns, rows)
    return new_room


@router.get("/rooms/{room_id}/", status_code=status.HTTP_200_OK, response_model=Room)
async def get_specific_room(db_room: Annotated[models.Room, Depends(get_room_by_id)]):
    """
        Getting specific room 
    """
    return db_room


@router.get("/rooms/", status_code=status.HTTP_200_OK, response_model=list[Room])
async def get_all_rooms(
        db: Annotated[Session, Depends(get_db)]):
    """
        Getting all rooms saved in the database
    """
    return db.query(models.Room).all()
