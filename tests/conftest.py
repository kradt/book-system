import pytest
import datetime
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from app import models
from app.main import app
from app.dependencies import get_db


@pytest.fixture()
async def client():
    """Async server client that handles lifespan and teardown"""
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client


db = pytest.fixture(get_db)


@pytest.fixture()
def room_json(db):
    necessary_dict = {
        "name": "Test Name Of Room",
        "seats": [
            {"row": 1, "column": 1, "number": 1, 'booked': False, 'additional_data': None}
            ],
        "events": [
            {"title": "The Film",
            "time_start": datetime.datetime(2020, 2, 1, 22, 30).isoformat(),
            "time_finish": datetime.datetime(2020, 2, 1, 23, 30).isoformat()
            }]
        }
    yield necessary_dict


@pytest.fixture(scope="function")
def created_room(db, room_json):
    seats = [models.Seat(**seat) for seat in room_json["seats"]]
    events = [models.Event(**event) for event in room_json["events"]]

    room = models.Room(name=room_json["name"])
    room.seats = seats
    room.events = events

    db.add(room)
    db.commit()
    yield room
    try:
        db.delete(room)
        db.commit()
    except Exception:
        pass