from pymongo import MongoClient
from pymongo.database import Database

from src.config import db_config


def get_db_connection() -> Database:
    """
        Create database connection to mongo engine

        Return
        ----------
        MongoClient
            Object containing the db connection
    """
    mongo_uri = db_config.get("MONGO_URI")
    mongo_db = db_config.get("MONGO_DB")

    return MongoClient(mongo_uri).get_database(mongo_db)
