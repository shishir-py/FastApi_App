from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL')

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        self.client = MongoClient(MONGODB_URL)
        self.db = self.client.crud_app
        self.collection = self.db.user
        print("Connected to MongoDB")

    def close(self):
        if self.client:
            self.client.close()
            print("Closed MongoDB connection")

# Create a global instance of the Database class
db = Database()

def get_collection():
    return db.collection

