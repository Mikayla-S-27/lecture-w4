# ECSE3038 - Week 4, Lecture 1 - starter
# Monday's API with the hard-coded list emptied.
# Run:  uvicorn app:app --reload

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import os # Allows python to interact with files on the computer
from dotenv import load_dotenv # Stores connection string in memory. So python knows connection string exists
from pymongo import MongoClient # Tells python how to connect to Mongo
from pymongo.errors import DuplicateKeyError

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI")) # Connects to the cluster
db = client["ecse3038"] # Creates database within the cluster
devices = db["devices"] # Creating a collection within the database

app = FastAPI()

class Device(BaseModel):
    name: str
    room: str
    temp: float
    online: bool

readings = []

@app.get("/devices")
def get_devices():
    return list(devices.find({},{"_id" : 0})) #First curly brackets is like a filter for the devices & second set specifies fields


@app.get("/devices/{name}")
def get_device(name: str):
    device = devices.find_one({"name": name}, {"_id" : 0})
    if device is None:
        raise HTTPException(status_code=404, detail="No device called " + name)
    return device


@app.post("/devices", status_code=201)
def create_device(device: Device):
    new_device = device.model_dump() # Convert device to dictionary
    try:
        devices.insert_one(new_device) # Insert new device to the database
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Device called " + new_device["name"] + " already exists")
    new_device.pop("_id")
    return new_device

