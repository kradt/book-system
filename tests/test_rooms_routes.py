import pytest

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

    response = await client.delete(f"/rooms/{created_room.id}/")
    assert response.status_code == 204
    assert not db.query(models.Room).filter_by(name=created_room.name).first()


@pytest.mark.asyncio
async def test_create_new_room_autogenerate(client, db, room_json):
    """
        Testing create new room with seat
    """
    response = await client.post("/rooms/?autogenerate=true&columns=2&rows=2", json=room_json)
    response_json = response.json()
    assert response.status_code == 201
    assert len(response_json["seats"]) == 4
    room_in_base = db.query(models.Room).filter_by(name=room_json["name"]).first()
    assert room_in_base
    assert len(room_in_base.seats) == 4

    response = await client.delete(f"/rooms/{room_in_base.id}/")
    assert response.status_code == 204
    assert not db.query(models.Room).filter_by(name=room_in_base.name).first()


@pytest.mark.asyncio
async def test_create_new_room_without_passing_autogenerate(client, db, room_json):
    """
        Testing create new room with seat
    """
    response = await client.post("/rooms/?autogenerate=true", json=room_json)
    response_json = response.json()
    assert response.status_code == 400
    assert response_json["detail"] == "For using autogenerating you have to pass count of columns and rows"


@pytest.mark.asyncio
async def test_create_new_room_with_the_same_name(client, db, room_json, created_room):
    """
        Testing create new room with seat
    """
    response = await client.post("/rooms/", json=room_json)
    response_json = response.json()
    assert response.status_code == 400
    assert response_json["detail"] == "The room with the same name alreadt exist"


@pytest.mark.asyncio
async def test_get_room_by_id(client, created_room):
    """
        Testing getting room by it id
    """
    room = await client.get(f"/rooms/{created_room.id}/")
    assert room.status_code == 200
    assert "name", "seats" in room.json()


@pytest.mark.asyncio
async def test_get_room_by_underfind_id(client, db):
    """
        Testing getting room by it id
    """
    room_id = -500
    response = await client.get(f"/rooms/{room_id}/")
    room_data = response.json()
    assert response.status_code == 404
    assert room_data["detail"] == "There is no such room"
    assert not db.query(models.Room).filter_by(id=room_id).first()


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
async def test_patch_query_to_rooms_with_alredy_exsiting_name(client, db, created_room):
    """
        Testing pathing room by id with exsisting name
    """
    name = "NEW TEST NAME"
    await client.post(f"/rooms/", json={"name": name})
    first_json_update = {
        "name": name
    }
    response = await client.patch(f"/rooms/{created_room.id}/", json=first_json_update)
    room = response.json()
    assert response.status_code == 400
    assert room["detail"] == "The room with the same name alreadt exist"

    room = db.query(models.Room).filter_by(name=name).first()
    await client.delete(f"/rooms/{room.id}/")
