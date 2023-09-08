import json
from fastapi import FastAPI, HTTPException, Query, Request
from pymongo import MongoClient
from bson import json_util
from datetime import datetime
from pydantic import BaseModel
from environ import environ

class envData:
    env = environ.Env()
    environ.Env.read_env()
    MONGO_DB_NAME = env('MONGO_INITDB_DATABASE')
    MONGO_DB_USER = env('MONGO_INITDB_ROOT_USERNAME')
    MONGO_DB_PASSWORD = env('MONGO_INITDB_ROOT_PASSWORD')
    MONGO_DB_COLLECTION = env('MONGO_DB_COLLECTION')

class DbAccess:
    def __init__(self):
        self.client = MongoClient(host="mongo_db", port=27017, username=envData.MONGO_DB_USER, password=envData.MONGO_DB_PASSWORD)
        self.db = self.client[envData.MONGO_DB_NAME]

    def connect_database(self):
        collection = self.db[envData.MONGO_DB_COLLECTION]
        return collection

    def close_database(self):
        self.client.close()

class Data_data(BaseModel):
    start: str
    end: str

app = FastAPI()

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
    connection = DbAccess()
    readings = connection.connect_database().find(query)
    json_data = [json.dumps(reading, default=json_util.default) for reading in readings]
    connection.close_database()
    return json_data

@app.get("/sensor/{sensor_id}")
def get_last_data(sensor_id: int):
    sensor_id_to_fetch = sensor_id
    projection = {"_id": 0}
    query = {"sensor_id": sensor_id_to_fetch}
    connection = DbAccess()
    documents = connection.connect_database().find(query, projection).sort([("time", -1)]).limit(10)
    json_data = [json.dumps(document, default=json_util.default) for document in documents]
    connection.close_database()
    return json_data

@app.get("/")
def read_root():
    return {"Hello World! Test from local"}