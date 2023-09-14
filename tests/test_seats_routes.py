import pytest

from app import models


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
async def test_update_specific_seat(client, db, created_room):
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

    third_json_update = {
        "booked": True
    }
    response = await client.patch(f"/rooms/{created_room.id}/seats/{created_room.seats[0].number}/", json=third_json_update)
    seat = response.json()
    assert response.status_code == 400
    assert seat["detail"] == "The seat already booked"
    assert not db.query(models.Seat).filter_by(id=created_room.seats[0].id).first().booked
