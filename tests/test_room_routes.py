import pytest
import datetime

from app import models


@pytest.mark.asyncio
async def test_create_new_room(client, db, room_json):
    """
        Testing create new room with seat
    """
    response = await client.post("/rooms/", json=room_json)
    response_json = response.json()
    assert response.status_code == 201
    assert room_json["name"] == response_json["name"]
    created_room = db.query(models.Room).filter_by(name=room_json["name"]).first()
    assert created_room
    assert created_room.seats
    assert created_room.events

    response = await client.delete(f"/rooms/{created_room.id}/")
    assert response.status_code == 204
    assert not db.query(models.Room).filter_by(name=created_room.name).first()


@pytest.mark.asyncio
async def test_get_room_by_id(client, created_room):
    """
        Testing getting room by it id
    """
    room = await client.get(f"/rooms/{created_room.id}/")
    print(room.json())
    assert room.status_code == 200
    assert "name", "seats" in room.json()


@pytest.mark.asyncio
async def test_get_all_rooms(client, created_room):
    """
        Testing getting all rooms
    """
    response = await client.get("/rooms/")
    rooms = response.json()
    assert response.status_code == 200
    assert "name", "seats" in rooms 
    assert isinstance(rooms, list)


@pytest.mark.asyncio
async def test_patch_query_to_rooms(client, created_room):
    """
        Testing pathing room by id
    """
    first_json_update = {
        "name": "New name"
    }
    response = await client.patch(f"/rooms/{created_room.id}/", json=first_json_update)
    room = response.json()
    assert response.status_code == 200
    assert room["name"] == first_json_update["name"]
    assert isinstance(room["seats"], list)
    assert len(room["seats"]) == 1
    second_json_update = {
        "seats": [
                {"row": 1, "column": 1, "number": 1},
                {"row": 1, "column": 2, "number": 2}
            ]
    }
    response = await client.patch(f"/rooms/{created_room.id}/", json=second_json_update)
    room = response.json()
    assert response.status_code == 200
    assert room["name"] == first_json_update["name"]
    assert isinstance(room["seats"], list)
    assert len(room["seats"]) == 2


@pytest.mark.asyncio
async def test_get_all_seats_specific_room(client, created_room):
    """
        Test getting seats of some room
    """
    response = await client.get(f"/rooms/{created_room.id}/seats/")
    seats = response.json()
    assert response.status_code == 200
    assert isinstance(seats, list)
    assert created_room.seats[0].row == seats[0]["row"]
    assert created_room.seats[0].column == seats[0]["column"]


@pytest.mark.asyncio
async def test_get_specific_seat_by_id(client, created_room):
    """
        Test getting specific seat by it id
    """
    response = await client.get(f"/rooms/{created_room.id}/seats/{created_room.seats[0].number}/")
    seat = response.json()
    assert response.status_code == 200
    assert created_room.seats[0].row == seat["row"]
    assert created_room.seats[0].column == seat["column"]


@pytest.mark.asyncio
async def test_update_specific_seat(client, created_room):
    """
        Test updating seat data
    """
    first_json_update = {
        "booked": True,
    }
    response = await client.patch(f"/rooms/{created_room.id}/seats/{created_room.seats[0].number}/", json=first_json_update)
    seat = response.json()
    assert response.status_code == 200
    assert seat["booked"] == first_json_update["booked"]

    second_json_update = {
        "additional_data": {"price": 2500}
    }
    response = await client.patch(f"/rooms/{created_room.id}/seats/{created_room.seats[0].number}/", json=second_json_update)
    seat = response.json()
    assert response.status_code == 200
    assert seat["booked"] == first_json_update["booked"]
    assert seat["additional_data"] == second_json_update["additional_data"]


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
async def test_getting_specific_event_by_it_id(client, db, created_room):
    """
        Test getting specific event by id
    """
    response = await client.get(f"/events/{created_room.events[0].id}/")
    event = response.json()
    assert response.status_code == 200
    assert event["title"] == created_room.events[0].title


@pytest.mark.asyncio
async def test_deleting_specific_event_by_id(client, db, created_room):
    """
        Test deleting specific event by it id
    """
    event_id = created_room.events[0].id
    response = await client.delete(f"/events/{event_id}/")
    assert response.status_code == 204
    assert not db.query(models.Event).filter_by(id=event_id).first()