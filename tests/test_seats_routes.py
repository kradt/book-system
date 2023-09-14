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
async def test_get_specific_seat_with_undefined_id(client, created_room):
    """
        Test getting specific seat by it id
    """
    number = -50
    response = await client.get(f"/rooms/{created_room.id}/seats/{number}/")
    seat = response.json()
    assert response.status_code == 404
    assert seat["detail"] == "There is no such seat"


@pytest.mark.asyncio
async def test_book_specific_seat(client, db, created_room):
    """
        Test updating seat data
    """
    json_update = {
        "booked": True
    }
    response = await client.patch(f"/rooms/{created_room.id}/seats/{created_room.seats[0].number}/", json=json_update)
    seat = response.json()
    assert response.status_code == 200
    assert seat["booked"] == json_update["booked"]

    seat_in_base = db.query(models.Seat).filter(
        models.Seat.number==created_room.seats[0].number,
        models.Seat.room_id==created_room.id
    ).first()

    db.refresh(seat_in_base)
    assert seat_in_base.number == seat["number"]
    assert seat["booked"] == seat_in_base.booked

    json_update = {
        "booked": True
    }
    response = await client.patch(f"/rooms/{created_room.id}/seats/{created_room.seats[0].number}/", json=json_update)
    seat = response.json()
    assert response.status_code == 400
    assert seat["detail"] == "The seat already booked"
    assert db.query(models.Seat).filter_by(id=created_room.seats[0].id).first().booked


@pytest.mark.asyncio
async def test_unbook_specific_seat(client, db, created_room):
    """
        Test unbook specific seat
    """
    json_update = {
        "booked": False
    }
    response = await client.patch(f"/rooms/{created_room.id}/seats/{created_room.seats[0].number}/", json=json_update)
    assert response.status_code == 200
    seat_in_base = db.query(models.Seat).filter_by(id=created_room.seats[0].id).first()
    db.refresh(seat_in_base)
    assert not seat_in_base.booked


@pytest.mark.asyncio
async def test_update_additional_data_of_specific_seat(client, db, created_room):
    json_update = {
        "additional_data": {"price": 2500}
    }
    response = await client.patch(f"/rooms/{created_room.id}/seats/{created_room.seats[0].number}/", json=json_update)
    seat = response.json()
    assert response.status_code == 200
    assert seat["additional_data"] == json_update["additional_data"]
