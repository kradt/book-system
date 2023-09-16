import datetime
import pytest

from app import models


@pytest.mark.asyncio
async def test_create_new_booking(client, db, booking_json):
    """
        Test creating new booking
    """
    response = await client.post("/booking/", json=booking_json)
    json = response.json()
    assert response.status_code == 201

    booking_in_base = db.query(models.Booking).filter_by(id=json["id"]).first()
    assert booking_in_base

    response = await client.delete(f"/booking/{json['id']}/")
    assert response.status_code == 204

    booking_in_base = db.query(models.Booking).filter_by(id=json["id"]).first()
    assert not booking_in_base
    

@pytest.mark.asyncio
async def test_create_new_booking_with_alredy_existing_time(client, db, created_booking, booking_json):
    response = await client.post("/booking/", json=booking_json)
    json = response.json()
    assert response.status_code == 400
    assert json["detail"] == "The Room has already had event it that time"


@pytest.mark.asyncio
async def test_create_new_booking_without_live_room(client, db, booking_json):
    db.delete(db.query(models.Room).filter_by(id=booking_json["room_id"]).first())
    db.commit()
    response = await client.post("/booking/", json=booking_json)
    json = response.json()
    assert response.status_code == 404
    assert json["detail"] == "The room with this id doesn't exist"


@pytest.mark.asyncio
async def test_create_new_booking_without_live_event(client, db, booking_json):
    db.delete(db.query(models.Event).filter_by(id=booking_json["event_id"]).first())
    db.commit()
    response = await client.post("/booking/", json=booking_json)
    json = response.json()
    assert response.status_code == 404
    assert json["detail"] == "The event with this id doesn't exist"


@pytest.mark.asyncio
async def test_get_all_booking(client, created_booking):
    """
        Test getting all bookings
    """
    response = await client.get("/booking/")
    json = response.json()
    assert response.status_code == 200
    assert isinstance(json, list)
    response = await client.get(f"/booking/?room_id={created_booking.room_id}")
    json = response.json()
    assert response.status_code == 200
    assert isinstance(json, list)
    response = await client.get(f"/booking/?event_id={created_booking.event_id}")
    json = response.json()
    assert response.status_code == 200
    assert isinstance(json, list)
    assert isinstance(json, list)


@pytest.mark.asyncio
async def test_delete_booking(client, db, created_booking):
    """
        Test deleting booking
    """
    response = await client.delete(f"/booking/{created_booking.id}/")
    assert response.status_code == 204
    booking_in_base = db.query(models.Booking).filter_by(id=created_booking.id).first()
    assert not booking_in_base


@pytest.mark.asyncio
async def test_patch_bookinng(client, db, created_booking):
    """
        Test Update booking
    """
    body_of_update = {
        "time_start": datetime.datetime(2000, 11, 10, 12, 35).isoformat(),
        "time_finish": datetime.datetime(2000, 11, 10, 14, 35).isoformat(),
        "additional_data": {"some_data": "some data hello world"}
    }
    response = await client.patch(f"/booking/{created_booking.id}/", json=body_of_update)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_patch_bookinng_with_booked_time(client, db, created_booking):
    """
        Test Update booking
    """
    body_of_update = {
        "time_start": created_booking.time_start,
        "time_finish": created_booking.time_start,
        "additional_data": created_booking.additional_data
    }
    response = await client.patch(f"/booking/{created_booking.id}/", json=body_of_update)
    json = response.json()
    assert response.status_code == 400
    assert json["detail"] == "The Room already have event it that time"


@pytest.mark.asyncio
async def test_patch_bookinng_with_only_one_param(client, db, created_booking):
    """
        Test Update booking
    """
    body_of_update = {
        "time_start": datetime.datetime.now().isoformat()
    }
    response = await client.patch(f"/booking/{created_booking.id}/", json=body_of_update)
    assert response.status_code == 200