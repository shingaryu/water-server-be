import os
from datetime import datetime

from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient

from common.get_logger import get_logger

load_dotenv()
logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

client = MongoClient('localhost', 27017)

db = client["waterServerDbDev"]
# logger.info('Successfully connected to database')

events_collection = db["Events"]

def find_recent_events(n_items):
    logger.info(f'Get first {n_items} events...')

    current_time = datetime.now()
    query = {"startTime": {"$gt": current_time}}
    sort_condition = [("startTime", pymongo.ASCENDING)]

    results = list(events_collection.find(query).sort(sort_condition).limit(n_items))

    for item in results:
        logger.debug(item)

    return results

# if __name__ == '__main__':
#     print('mongo_repository:main')
#     find_recent_events(2)
