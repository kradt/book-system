import datetime
import pytest

from app import models


@pytest.mark.asyncio
async def test_get_all_events_specific_room_by_room_id(client, created_room):
    """
        Test getting all event events of some room
    """
    response = await client.get(f"/rooms/{created_room.id}/events/")
    rooms = response.json()
    assert response.status_code == 200
    assert len(rooms) == 1
    assert created_room.events[0].title == rooms[0]["title"]


@pytest.mark.asyncio
async def test_create_event_for_specific_room(client, db, created_room):
    """
        Test creating event for specific room
    """
    body = {
        "title": "The Big Lebovski",
        "time_start": datetime.datetime.now().isoformat(),
        "time_finish": datetime.datetime.now().isoformat(),
        "additional_data": {}
    }
    response = await client.post(f"/rooms/{created_room.id}/events/", json=body)
    response_json = response.json()
    assert response.status_code == 201
    event_in_base = db.query(models.Event).filter_by(title=body["title"]).first()
    assert event_in_base.title == response_json["title"]
    assert event_in_base.time_start.isoformat() == response_json["time_start"]
    assert event_in_base.time_finish.isoformat() == response_json["time_finish"]
    response = await client.delete(f"/events/{event_in_base.id}/")
    assert response.status_code == 204
    event_in_base = db.query(models.Event).filter_by(title=body["title"]).first()
    assert not event_in_base


@pytest.mark.asyncio
async def test_create_event_for_specific_room_with_event_in_interval(client, db, created_room):
    """
        Test creating event for specific room
    """
    body = {
        "title": "NEW FILM",
        "time_start": created_room.events[0].time_start,
        "time_finish": created_room.events[0].time_finish,
        "additional_data": {}
    }
    response = await client.post(f"/rooms/{created_room.id}/events/", json=body)
    response_json = response.json()
    assert response.status_code == 400
    assert response_json["detail"] == "The Room already have event it that time"


@pytest.mark.asyncio
async def test_create_event_for_specific_room_with_already_existing_name(client, db, created_room):
    """
        Test creating event for specific room
    """
    body = {
        "title": created_room.events[0].title,
        "time_start": datetime.datetime.now().isoformat(),
        "time_finish": datetime.datetime.now().isoformat(),
        "additional_data": {}
    }
    response = await client.post(f"/rooms/{created_room.id}/events/", json=body)
    response_json = response.json()
    assert response.status_code == 400
    assert response_json["detail"] == "The event with the same name already exist"


@pytest.mark.asyncio
async def test_getting_specific_event_by_it_id(client, db, created_room):
    """
        Test getting specific event by id
    """
    response = await client.get(f"/events/{created_room.events[0].id}/")
    event = response.json()
    assert response.status_code == 200
    assert event["title"] == created_room.events[0].title


@pytest.mark.asyncio
async def test_getting_specific_undefind_event(client, db):
    event_id = -150
    response = await client.get(f"/events/{event_id}/")
    event_data = response.json()
    assert response.status_code == 404
    assert event_data["detail"] == "There is no such event"
    event_in_base = db.query(models.Event).filter_by(id=event_id).first()
    assert not event_in_base


@pytest.mark.asyncio
async def test_deleting_specific_event_by_id(client, db, created_room):
    """
        Test deleting specific event by it id
    """
    event_id = created_room.events[0].id
    response = await client.delete(f"/events/{event_id}/")
    assert response.status_code == 204
    assert not db.query(models.Event).filter_by(id=event_id).first()
