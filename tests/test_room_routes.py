import pytest


@pytest.mark.asyncio
async def test_create_new_room(client, room_json):
    response = await client.post("/rooms/", json=room_json)
    print(response)
    print(response.json())

    assert response.status_code == 201
    assert room_json == response.json()
