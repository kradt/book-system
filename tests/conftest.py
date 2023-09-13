import pytest
from bson import ObjectId
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from app import models, SessionLocal
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
        "events": []
    }
    yield necessary_dict
    room_in_base = db.query(models.Room).filter_by(name=necessary_dict["name"]).first()
    if room_in_base:
        db.delete(room_in_base)
        db.commit()


@pytest.fixture(scope="function")
def created_room(client, db, room_json):
    seats = [models.Seat(**seat) for seat in room_json["seats"]]
    events = [models.Event(**event) for event in room_json["events"]]

    room = models.Room(name=room_json["name"])
    room.seats = seats
    room.events = events

    db.add(room)
    db.commit()
    yield room
    for seat in room.seats:
        db.delete(seat)
    db.delete(room)
    db.commit()
