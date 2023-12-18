import os
from datetime import datetime
from bson import ObjectId
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient

from common.get_logger import get_logger

load_dotenv()
logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

logger.debug(f'MongoDB Connection to {os.environ.get("CONNECTION_STRING")}...')
client = MongoClient(os.environ.get("CONNECTION_STRING"), tlsAllowInvalidCertificates=True)

db = client[os.environ.get("DB_NAME")]
# logger.info('Successfully connected to database')

events_collection = db["Events"]
entries_collection = db["Entries"]

def find_recent_events(n_items):
    logger.info(f'Get first {n_items} events...')

    current_time = datetime.now()
    query = {"endTime": {"$gt": current_time}}
    sort_condition = [("endTime", pymongo.ASCENDING)]

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

# This function returns all users in a specific event.
# The returned dict contains only one same user for the event.
# (e.g. There could be multiple entries for a user. like they updated their attendance.
# This function returns only one user for them.)
def find_all_members_in_the_event(event_id: ObjectId) -> dict:
    id: str = str(event_id)
    #For test TODO: delete here
    # id = "64616a5af743fbf3cfa47cc8" #an event in Nov.
    
    entries: list = list(entries_collection.find({"eventId": id}))
    results: dict = dict()
    for entry in entries:
        key: str = entry["user"]["userId"]
        value = entry["user"]
        results[key] = value
        
    return results

def find_entry(event_id, user_id):
    logger.info(f'Find entry with event_id: {event_id}, user id: {user_id}...')
    entry = entries_collection.find_one({"eventId": event_id, "user.userId": user_id})
    logger.debug(entry)

    return entry

def insert_entry(document):
    logger.info(f'Insert entry...')
    result = entries_collection.insert_one(document)
    logger.debug(f'New document id: {result.inserted_id}')
    return result

def delete_entry(id):
    logger.info(f'Delete entry: {str(id)}...')
    filter = {"_id": id}
    result = entries_collection.delete_one(filter)

    logger.debug(f'{result.deleted_count} document(s) deleted')
    return result

def update_event(oid, field_dict_to_update):
    logger.info(f'Update event {str(oid)} with {field_dict_to_update}...')
    filter = {"_id": oid}
    update = {'$set': field_dict_to_update}
    result = events_collection.update_one(filter, update)
    logger.debug(f'{result.matched_count} event(s) matched, {result.modified_count} event(s) modified')
    return result

# if __name__ == '__main__':
#     print('mongo_repository:main')
#     find_recent_events(2)
