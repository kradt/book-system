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
def room_json():
    necessary_dict = {
        "name": "Test Name Of Room",
        "seats": [
            {"row": 1, "column": 1, "number": 1, 'booked': False, 'additional_data': None}
            ]
        }
    yield necessary_dict


@pytest.fixture(scope="function")
def created_room(db, room_json):
    seats = [models.Seat(**seat) for seat in room_json["seats"]]

    room = models.Room(name=room_json["name"])
    room.seats = seats

    db.add(room)
    db.commit()
    yield room
    try:
        [db.delete(book) for book in room.booking]
        db.delete(room)
        db.commit()
    except Exception as e:
        print(e)
        pass


@pytest.fixture(scope="function")
def created_event(db):
    info = {
        "name": "Some name for Event",
        "additional_data": {}
    }
    new_event = models.Event(title=info["name"], additional_data=info["additional_data"])
    db.add(new_event)
    db.commit()
    yield new_event
    try:
        [db.delete(book) for book in new_event.booking]
        db.delete(new_event)
        db.commit()
    except Exception as e:
        print(e)
        pass


@pytest.fixture(scope="function")
def booking_json(db, created_room, created_event):
    necessary_dict = {
        "room_id": created_room.id,
        "event_id": created_event.id,
        "time_start": datetime.datetime.now().isoformat(),
        "time_finish": datetime.datetime.now().isoformat()
    }
    yield necessary_dict


@pytest.fixture(scope="function")
def created_booking(db, booking_json):
    new_bookinng = models.Booking(
        room_id=booking_json["room_id"],
        event_id=booking_json["event_id"],
        time_start=booking_json["time_start"],
        time_finish=booking_json["time_finish"]
    )
    db.add(new_bookinng)
    db.commit()
    yield new_bookinng
    try:
        db.delete(new_bookinng)
        db.commit()
    except Exception:
        pass
