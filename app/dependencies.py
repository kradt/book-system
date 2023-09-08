from fastapi import HTTPException

from app import models


async def get_room(room_id):
    room = await models.Room.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="There is no such room")
    return room