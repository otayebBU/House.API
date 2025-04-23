from fastapi.testclient import TestClient
from house import app  


client = TestClient(app)

def test_create_user():
    response = client.post("/users?name=TestUser")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "TestUser"

def test_create_house_for_user():
    user_resp = client.post("/users?name=Owner")
    user_id = user_resp.json()["id"]

    house_resp = client.post(f"/users/{user_id}/houses?name=SmartHome")
    assert house_resp.status_code == 200
    house_data = house_resp.json()
    assert house_data["name"] == "SmartHome"
    assert "id" in house_data

def test_create_room_for_house():
    user_resp = client.post("/users?name=Tester")
    user_id = user_resp.json()["id"]

    house_resp = client.post(f"/users/{user_id}/houses?name=TestHouse")
    house_id = house_resp.json()["id"]

    room_resp = client.post(f"/houses/{house_id}/rooms?name=Bedroom")
    assert room_resp.status_code == 200
    room_data = room_resp.json()
    assert room_data["name"] == "Bedroom"

def test_add_device_to_room():
    user_resp = client.post("/users?name=DeviceTester")
    user_id = user_resp.json()["id"]

    house_resp = client.post(f"/users/{user_id}/houses?name=House1")
    house_id = house_resp.json()["id"]

    room_resp = client.post(f"/houses/{house_id}/rooms?name=Room1")
    room_id = room_resp.json()["id"]

    device_resp = client.post(f"/rooms/{room_id}/devices?name=Sensor1&type=Temperature")
    assert device_resp.status_code == 200
    device_data = device_resp.json()
    assert device_data["name"] == "Sensor1"
    assert device_data["type"] == "Temperature"
