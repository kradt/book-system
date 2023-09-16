import pytest

from app import models


@pytest.mark.asyncio
async def test_get_all_events_specific_room_by_room_id(client, created_room):
    """
        Test getting all event events of some room
    """
    response = await client.get(f"/events/")
    rooms = response.json()
    assert response.status_code == 200
    assert isinstance(rooms, list)


@pytest.mark.asyncio
async def test_create_event(client, db, created_room):
    """
        Test creating event for specific room
    """
    body = {
        "title": "The Big Lebovski",
        "additional_data": {}
    }
    response = await client.post(f"/events/", json=body)
    response_json = response.json()
    assert response.status_code == 201
    event_in_base = db.query(models.Event).filter_by(title=body["title"]).first()
    assert event_in_base.title == response_json["title"]
    response = await client.delete(f"/events/{event_in_base.id}/")
    assert response.status_code == 204
    event_in_base = db.query(models.Event).filter_by(title=body["title"]).first()
    assert not event_in_base


@pytest.mark.asyncio
async def test_create_event_with_already_existing_name(client, db, created_event):
    """
        Test creating event for specific room
    """
    body = {
        "title": created_event.title,
        "additional_data": {}
    }
    response = await client.post(f"/events/", json=body)
    response_json = response.json()
    assert response.status_code == 400
    assert response_json["detail"] == "The event with the same name already exist"


@pytest.mark.asyncio
async def test_getting_specific_event_by_it_id(client, created_event):
    """
        Test getting specific event by id
    """
    response = await client.get(f"/events/{created_event.id}/")
    event = response.json()
    print(event)
    assert response.status_code == 200
    assert event["title"] == created_event.title


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
async def test_deleting_specific_event_by_id(client, db, created_event):
    """
        Test deleting specific event by it id
    """
    event_id = created_event.id
    response = await client.delete(f"/events/{event_id}/")
    assert response.status_code == 204
    assert not db.query(models.Event).filter_by(id=event_id).first()
