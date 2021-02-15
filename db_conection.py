from pymongo import MongoClient
import config

client = MongoClient(config.config.db_conection_pymongo.host(), config.config.db_conection_pymongo.port())
db = client[config.config.db_conection_pymongo.db_name()]
users = db[config.config.db_conection_pymongo.collection()]