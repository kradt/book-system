import pytest
from app import models


@pytest.mark.asyncio
async def test_create_new_room(client, room_json):
    """
        Testing create new room with seat
    """
    response = await client.post("/rooms/", json=room_json)
    assert response.status_code == 201
    assert room_json == response.json()
    created_room = await models.Room.find_one({"name": room_json["name"]})
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
async def test_delete_specific_room(client, created_room):
    """
        Testing deleting room by it id
    """
    response = await client.delete(f"/rooms/{created_room.id}")
    assert response.status_code == 204
    assert not await models.Room.find_one({"name": created_room.name})


@pytest.mark.asyncio
async def test_patch_query_to_rooms(client, created_room):
    """
        Testing pathing room by id
    """
    first_json_update = {
        "name": "New name"
    }
    response = await client.patch(f"/rooms/{created_room.id}", json=first_json_update)
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
    response = await client.patch(f"/rooms/{created_room.id}", json=second_json_update)
    room = response.json()
    assert response.status_code == 200
    assert room["name"] == first_json_update["name"]
    assert isinstance(room["seats"], list)
    assert len(room["seats"]) == 2

    
