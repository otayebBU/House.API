from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from uuid import uuid4

app = FastAPI()

class Device(BaseModel):
    id: str
    name: str
    type: str  # Temperature or Humidity

class Room(BaseModel):
    id: str
    name: str
    devices: List[Device] = []

class House(BaseModel):
    id: str
    name: str
    rooms: List[Room] = []

class User(BaseModel):
    id: str
    name: str
    houses: List[House] = []


users: Dict[str, User] = {}


@app.post("/users", response_model=User)
def create_user(name: str):
    user = User(id=str(uuid4()), name=name)
    users[user.id] = user
    return user

@app.get("/users", response_model=List[User])
def list_users():
    return list(users.values())

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    if user_id in users:
        return users[user_id]
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    if user_id in users:
        del users[user_id]
        return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")



@app.post("/users/{user_id}/houses", response_model=House)
def create_house(user_id: str, name: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    house = House(id=str(uuid4()), name=name)
    users[user_id].houses.append(house)
    return house

@app.get("/users/{user_id}/houses", response_model=List[House])
def list_houses(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id].houses


@app.delete("/houses/{house_id}")
def delete_house(house_id: str):
    for user in users.values():
        for house in user.houses:
            if house.id == house_id:
                user.houses.remove(house)
                return {"message": "House deleted"}
    raise HTTPException(status_code=404, detail="House not found")


@app.post("/houses/{house_id}/rooms", response_model=Room)
def create_room(house_id: str, name: str):
    for user in users.values():
        for house in user.houses:
            if house.id == house_id:
                room = Room(id=str(uuid4()), name=name)
                house.rooms.append(room)
                return room
    raise HTTPException(status_code=404, detail="House not found")

@app.get("/houses/{house_id}/rooms", response_model=List[Room])
def list_rooms(house_id: str):
    for user in users.values():
        for house in user.houses:
            if house.id == house_id:
                return house.rooms
    raise HTTPException(status_code=404, detail="House not found")


@app.delete("/rooms/{room_id}")
def delete_room(room_id: str):
    for user in users.values():
        for house in user.houses:
            for room in house.rooms:
                if room.id == room_id:
                    house.rooms.remove(room)
                    return {"message": "Room deleted"}
    raise HTTPException(status_code=404, detail="Room not found")



@app.post("/rooms/{room_id}/devices", response_model=Device)
def add_device_to_room(room_id: str, name: str, type: str):
    device = Device(id=str(uuid4()), name=name, type=type)
    for user in users.values():
        for house in user.houses:
            for room in house.rooms:
                if room.id == room_id:
                    room.devices.append(device)
                    return device
    raise HTTPException(status_code=404, detail="Room not found")

@app.get("/rooms/{room_id}/devices", response_model=List[Device])
def list_devices(room_id: str):
    for user in users.values():
        for house in user.houses:
            for room in house.rooms:
                if room.id == room_id:
                    return room.devices
    raise HTTPException(status_code=404, detail="Room not found")

@app.delete("/devices/{device_id}")
def delete_device(device_id: str):
    for user in users.values():
        for house in user.houses:
            for room in house.rooms:
                for device in room.devices:
                    if device.id == device_id:
                        room.devices.remove(device)
                        return {"message": "Device deleted"}
    raise HTTPException(status_code=404, detail="Device not found")


# endpoint (endpoint is one end of a communication channel )



