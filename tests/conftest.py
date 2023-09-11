import pytest
from bson import ObjectId
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from app import models
from app.main import app

        
@pytest.fixture()
async def client():
    """Async server client that handles lifespan and teardown"""
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client


@pytest.fixture()
async def room_json(client):
    necessary_dict = {"name": "First Room", "seats": [{"row": 1, "column": 1, "number": 1, 'booked': False, 'additional_data': None,}]}
    yield necessary_dict
    room = models.Room.find_one({"name": necessary_dict["name"]})
    if room:
        await room.delete()


@pytest.fixture()
async def created_room(client, room_json):
    room = models.Room(_id=ObjectId(), **room_json)
    await room.create()
    yield room
    await room.delete()
