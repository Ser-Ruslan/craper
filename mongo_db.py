import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = "books_scraper"
LINKS_COLLECTION = "scraping_links"
BOOKS_COLLECTION = "extracted_books"

class MongoDBConnection:
    def __init__(self):
        self.client = None
        self.db = None
        self.links_collection = None
        self.books_collection = None
    
    def connect(self):
        try:
            self.client = MongoClient(MONGO_URI)
            self.client.admin.command('ping')
            self.db = self.client[DATABASE_NAME]
            self.links_collection = self.db[LINKS_COLLECTION]
            self.books_collection = self.db[BOOKS_COLLECTION]
            
            # индексы
            self.links_collection.create_index("url", unique=True)
            self.books_collection.create_index("url", unique=True)
            
            print("Подключено к MongoDB")
            return True
        except ConnectionFailure as e:
            print(f"Ошибка подключения к MongoDB: {e}")
            return False
    
    def close(self):
        if self.client:
            self.client.close()
            print("Соединение с MongoDB закрыто")
    
    def get_links_collection(self):
        return self.links_collection
    
    def get_books_collection(self):
        return self.books_collection


mongo_db = MongoDBConnection()

def get_mongo_connection():
    return mongo_db
