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
entries_collection = db["Entries"]

def find_recent_events(n_items):
    logger.info(f'Get first {n_items} events...')

    current_time = datetime.now()
    query = {"startTime": {"$gt": current_time}}
    sort_condition = [("startTime", pymongo.ASCENDING)]

    results = list(events_collection.find(query).sort(sort_condition).limit(n_items))

    for item in results:
        logger.debug(item)

    return results

def find_all_events():
    logger.info('Find all events...')
    results = list(events_collection.find())

    return results

def find_event(event_id):
    logger.info(f'Find event with id: {event_id}...')
    event = events_collection.find_one({"_id": event_id})

    if event:
        logger.debug(event)

    return event

def find_all_entries():
    logger.info('Find all entries...')
    results = list(entries_collection.find())

    return results
# if __name__ == '__main__':
#     print('mongo_repository:main')
#     find_recent_events(2)
