import json
from typing import Union
from fastapi import FastAPI, HTTPException, Query, Request
from pymongo import MongoClient
from bson import json_util
from datetime import datetime
from pydantic import BaseModel

class Data_data(BaseModel):
    start: str
    end: str

app = FastAPI()

def connect_database():
    client = MongoClient(host="mongo_db", port=27017, username="root", password="rootpassword")
    db = client['test']
    table = db.test_table
    return table

@app.get("/sensor/{sensor_id}")
def get_last_data(sensor_id: int):
    sensor_id_to_fetch = sensor_id

    projection = {"_id": 0}
    query = {"sensor_id": sensor_id_to_fetch}
    documents = connect_database().find(query, projection).sort([("time", -1)]).limit(10)
    json_data = [json.dumps(document, default=json_util.default) for document in documents]
    return json_data

@app.get("/fetch_sensor_readings/")
async def fetch_sensor_readings(data: Data_data):
    try:
        print("Start time:", data.start)
        print("End time:", data.end)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format")

    # Query MongoDB for data within the specified range
    query = {
        "time": {"$gte": data.start, "$lte": data.end}
    }
    readings = connect_database().find(query)
    json_data = [json.dumps(reading, default=json_util.default) for reading in readings]
    return json_data

@app.get("/")
def read_root():
    return {"Hello": "World Test from local"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

