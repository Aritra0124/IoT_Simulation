from pymongo import MongoClient

def save_data(data):
    client = MongoClient(host="mongo_db", port=27017, username="root", password="rootpassword")
    db = client['test']
    table = db.test_table
    save = table.insert_one(data)
    print("data saved ->",save)
    client.close()