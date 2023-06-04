# mongo_repository.update_eventの使い方例。

from bson import ObjectId
from dotenv import load_dotenv
from repositories.mongo_repository import update_event

load_dotenv()

if __name__ == '__main__':
    print('mongo_repository:main')
    oid = ObjectId('646ccdbbcf2b2db5b687a315') # find_recent_events(n_items)の返り値から取り出す場合、events[0]["_id"]
    field_to_update = {'isReminded': True}
    update_event(oid, field_to_update)