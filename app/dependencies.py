from fastapi import HTTPException, Depends, Path
from typing import Annotated 
from beanie.odm.operators.find.logical import Or, And


from app import models


async def get_room_by_id(room_id: str):
    """
        Depends that useing for getting specific room
    """
    room = await models.Room.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="There is no such room")
    return room


async def get_seat_by_number(
        db_room: Annotated[models.Room, Depends(get_room_by_id)], 
        seat_number: Annotated[int, Path(title="Number of seat in the room")]):
    """
        Depends that using for getting specific seat
    """
    return await models.Seat.find_one({"number": seat_number})


async def get_event_by_id(event_id: str):
    event = await models.Event.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="There is no such events")
    return event