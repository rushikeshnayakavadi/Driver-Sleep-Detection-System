# src/database/mongodb_client.py

from pymongo import MongoClient

class MongoDBClient:
    def __init__(self):
        try:
            # self.mongo_uri = "mongodb+srv://rushikeshnayakavadi:KoppEuYvJKrnXQyI@project1.137egka.mongodb.net/?retryWrites=true&w=majority&appName=project1"
            self.mongo_uri ="mongodb+srv://rushikeshnayakavadi:KoppEuYvJKrnXQyI@project1.137egka.mongodb.net/?retryWrites=true&w=majority&appName=project1"
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client["driver_sleep"]
            print("Connected to MongoDB")
        except Exception as e:
            print("Error connecting to MongoDB:", e)
            raise e

    def get_database(self):
        return self.db

if __name__ == "__main__":
    mongo = MongoDBClient()
    db = mongo.get_database()
    print("Database object fetched:", db.name)
