from pymongo import MongoClient
from source.config import db_config

client = MongoClient(db_config.get("MONGO_URI"))

db = client["admin"]

users = db['users']
