from pymongo import MongoClient
from src.core.env import Settings
settings = Settings()

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]
