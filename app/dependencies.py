from fastapi import HTTPException, Depends, Path
from typing import Annotated

from app import models


async def get_room_by_id(room_id):
    room = await models.Room.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="There is no such room")
    return room


def get_seat_by_number(
        db_room: Annotated[models.Room, Depends(get_room_by_id)], 
        seat_number: Annotated[int, Path(title="Number of seat in the room")]):
    
    if seat_number > len(db_room.seats) or seat_number <= 0:
        raise HTTPException(404, "Seat with this number doesn't exist")
    return db_room.seats[seat_number-1]
    