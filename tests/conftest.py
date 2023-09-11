import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from app import models, config
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
        