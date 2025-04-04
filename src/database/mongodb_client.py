from pymongo import MongoClient

class MongoDBClient:
    def __init__(self):
        try:
            self.mongo_uri = "mongodb+srv://rushikeshnayakavadi:KoppEuYvJKrnXQyI@project1.137egka.mongodb.net/?retryWrites=true&w=majority&appName=project1"
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client["driver_sleep_detection"]  # Use your real database name
            print("Connected to MongoDB")
        except Exception as e:
            print("Error connecting to MongoDB:", e)
            raise e

    def get_database(self):
        return self.db
