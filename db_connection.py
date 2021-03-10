import jsoncfg
from pymongo import MongoClient


db_config = jsoncfg.load_config('db_config.cfg')

client = MongoClient(
    db_config.host(),
    db_config.port()
    )

db = client[db_config.db_name()]
users = db[db_config.collection()]