from pymongo import MongoClient
import config


client = MongoClient(
    config.config.db_connection_pymongo.host(),
    config.config.db_connection_pymongo.port()
    )

db = client[config.config.db_connection_pymongo.db_name()]
users = db[config.config.db_connection_pymongo.collection()]