from fastapi import FastAPI, HTTPException, Query, Request
from pymongo import MongoClient
from pydantic import BaseModel
import os
class envData:
    MONGO_DB_NAME = os.getenv('MONGO_INITDB_DATABASE')
    MONGO_DB_USER = os.getenv('MONGO_INITDB_ROOT_USERNAME')
    MONGO_DB_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
    MONGO_DB_COLLECTION = os.getenv('MONGO_DB_COLLECTION')

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

@app.get("/fetch_readings/")
async def fetch_sensor_readings(data: Data_data):
    try:
        print("Start time:", data.start)
        print("End time:", data.end)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format")

    # Query MongoDB for data within the specified range
    projection = {"_id": 0}
    query = {
        "timestamp": {"$gte": data.start, "$lte": data.end}
    }
    connection = DbAccess()
    record_count = connection.connect_database().count_documents(query)
    documents = list(connection.connect_database().find(query, projection))
    connection.close_database()
    return {"count": record_count, "records": documents}

@app.get("/sensor/{sensor_id}")
def get_last_data(sensor_id: int):
    sensor_id_to_fetch = sensor_id
    projection = {"_id": 0}
    query = {"sensor_id": sensor_id_to_fetch}
    connection = DbAccess()
    documents = list(connection.connect_database().find(query, projection).sort([("time", -1)]).limit(10))
    connection.close_database()
    return documents

@app.get("/")
def read_root():
    return {"Hello World! Test from local"}