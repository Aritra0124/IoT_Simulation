from pymongo import MongoClient
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

def save_data(data):
    connection = DbAccess()
    save = connection.connect_database().insert_one(data)
    connection.close_database()