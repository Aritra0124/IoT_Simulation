import ast
import json

from pymongo import MongoClient

def save_data(data):
    client = MongoClient(host="mongo_db", port=27017, username="root", password="rootpassword")
    db = client['test']
    table = db.test_table
    print("dict data type ->",data)
    print(type(data))
    save = table.insert_one(data)
    print(save)
    client.close()