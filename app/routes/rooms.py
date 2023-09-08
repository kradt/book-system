from fastapi import APIRouter, Path, status, Depends, HTTPException
from typing import Annotated
from bson import ObjectId

from app.schemas.rooms import Room, RoomUpdate, RoomOutput
from app.schemas.places import Place
from app.dependencies import get_room
from app import models


router = APIRouter(tags=["Rooms"])


@router.get("/rooms/{room_id}/places/{place_number}/book", status_code=200, response_model=Place)
async def book_a_place(
        db_room: Annotated[models.Room, Depends(get_room)], 
        place_number: Annotated[int, Path(title="number of seat in the room")]):
    
    place = db_room.places[place_number-1]
    place.booked = True
    await db_room.save()
    return place

@router.get("/rooms/{room_id}/places/{place_number}/", status_code=200, response_model=list[Place])
def get_specific_room(
        db_room: Annotated[models.Room, Depends(get_room)], 
        place_number: Annotated[int, Path(title="number of seat in the room")]):
    
    return db_room.places[place_number-1]

@router.get("/rooms/{room_id}/places/", status_code=200, response_model=list[Place])
def get_places_specific_room(db_room: Annotated[models.Room, Depends(get_room)]):
    return db_room.places


@router.get("/rooms/{room_id}", status_code=status.HTTP_200_OK, response_model=RoomOutput)
async def get_specific_room(room_id: Annotated[str, Path(title="The id of specific room")]):
    """
        Getting specific room 
    """
    return await models.Room.get(room_id)


@router.patch("/rooms/{room_id}", status_code=status.HTTP_200_OK, response_model=RoomOutput)
async def update_room_info(
    room: RoomUpdate,
    db_room: Annotated[models.Room, Depends(get_room)]):
    """
        Update room info
    """
    await db_room.set({"name": room.name})
    return db_room


@router.delete("/rooms/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
        db_room: Annotated[models.Room, Depends(get_room)]):
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


@router.get("/rooms/", status_code=status.HTTP_200_OK, response_model=list[RoomOutput])
async def get_all_rooms():
    """
        Getting all rooms saved in the database
    """
    return await models.Room.find_all().to_list()
