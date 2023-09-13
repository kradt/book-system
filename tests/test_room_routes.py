import pytest
import datetime

from app import models


@pytest.mark.asyncio
async def test_create_new_room(client, db, room_json):
    """
        Testing create new room with seat
    """
    response = await client.post("/rooms/", json=room_json)
    assert response.status_code == 201
    assert room_json == response.json()
    created_room = db.query(models.Room).filter_by(name=room_json["name"]).first()
    assert created_room
    assert created_room.seats


@pytest.mark.asyncio
async def test_get_room_by_id(client, created_room):
    """
        Testing getting room by it id
    """
    room = await client.get(f"/rooms/{created_room.id}/")
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
async def test_delete_specific_room(db, client, created_room):
    """
        Testing deleting room by it id
    """
    response = await client.delete(f"/rooms/{created_room.id}/")
    assert response.status_code == 204
    assert not db.query(models.Room).filter_by(name=created_room.name).first()


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
    print(seat)
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
    pass


@pytest.mark.asyncio
async def test_create_event_for_specific_room(client, db, created_room):
    """
        Test creating event for specific room
    """
    body = {
        "title": "The Big Lebovski",
        "time_start": str(datetime.datetime(2022, 1, 2, 13, 00)),
        "time_finish": str(datetime.datetime(2022, 1, 2, 14, 00))
    }
    response = await client.post(f"/rooms/{created_room.id}/events/", json=body)
    print(response.json())
    assert response.status_code == 201
    event_in_base = db.query(models.Event).filter_by(title=body["title"])
    assert event_in_base.title == response.title
    assert event_in_base.time_start == response.time_start
    assert event_in_base.time_finish == response.time_finish



