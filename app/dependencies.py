from fastapi import HTTPException, Depends, Path
from typing import Annotated 
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, engine


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
   
    """
        TODO: getting room 
    """
    return room


async def get_event_by_id(event_id: str):
    event = await models.Event.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="There is no such events")
    return event


async def get_session():
    async with AsyncSession(bind=engine, expire_on_commit=False) as async_session:
        yield async_session