import os
import random

from flask import url_for
from linebot.models import FlexSendMessage, TextSendMessage, ImageSendMessage
from common.consts import SELECT_EVENT_TO_ENTRY, SELECT_EVENT_TO_ENTRY_EVENT
from common.get_logger import get_logger
from repositories.mongo_repository import find_recent_events, find_all_events, find_all_entries, find_event, find_entry, \
    insert_entry, delete_entry
from set_webhook_url import PUBLIC_URL_ENV_KEY
from templates.select_entry_events_template import event_flex_contents, select_event_message_contents
from templates.select_option_to_entry_template import select_option_to_entry_flex_contents

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))
public_url = os.environ.get(PUBLIC_URL_ENV_KEY)

N_RECENT_EVENTS = 5

def show_recent_event_message():
    events = find_recent_events(1)
    if len(events) == 0:
        return TextSendMessage(text='直近の開催予定がありません。')
    else:
        return select_option_to_entry_message(events[0]["_id"])

def select_entry_events_message():
    event_contents = []
    recent_events = find_recent_events(N_RECENT_EVENTS)
    for event in recent_events:
        postback_data = f'{SELECT_EVENT_TO_ENTRY}/?{SELECT_EVENT_TO_ENTRY_EVENT}={str(event["_id"])}'
        this_event_contents = event_flex_contents(event["startTime"], event["place"], 0,
                                                  postback_data)
        event_contents += this_event_contents

    contents = select_event_message_contents(N_RECENT_EVENTS, event_contents)
    flex_message = FlexSendMessage(
        alt_text='開催一覧',
        contents=contents
    )

    return flex_message

def select_option_to_entry_message(event_id):
    event = find_event(event_id)
    entries = find_all_entries()

    dict = {}
    for option in event["entryOptions"]:
        dict[str(option["id"])] = (option, [])

    for entry in entries:
        if entry["eventId"] != str(event_id):
            continue

        (opt, attendees_list) = dict[entry["selectedOptionId"]]
        attendees_list.append(entry["user"])

    contents = select_option_to_entry_flex_contents(event, list(dict.values()))

    flex_message = FlexSendMessage(
        alt_text='投票する',
        contents=contents
    )

    return flex_message

def entry_with_option(event_id, option_id, user):
    document_data = {
        "eventId": event_id,
        "user": {
            "userId": user.user_id,
            "displayName": user.display_name,
            "pictureUrl": user.picture_url,
            "statusMessage": user.status_message
        },
        "selectedOptionId": option_id
    }

    user_entry = find_entry(event_id, user.user_id)
    message = None
    if user_entry:
        # delete existing
        delete_entry(user_entry["_id"])
        result = insert_entry(document_data)

        message = TextSendMessage(text=f'再投票しました。')
    else:
        result = insert_entry(document_data)
        message = TextSendMessage(text=f'投票しました。')

    return message

def album_message():
    logger.info('album_message')

    # サンプル画像での例。staticフォルダ内にファイルを置くことで外部に公開できる。
    # ここではalbumフォルダ内に画像ファイルを対応するサムネイルとセットで置き、ランダムに一つ選んでいる
    # Todo: フォルダ内の全ファイル名を取得し、ランダムに一つ選ぶ。このとき、元画像と_thumbを末尾に持つファイルをセットで取得する。
    sample_photo_sets = [
        {
            "original": "IMG_0691.JPG",
            "thumbnail": "IMG_0691_thumb.JPG"
        },
        {
            "original": "IMG_0734.JPG",
            "thumbnail": "IMG_0734_thumb.JPG"
        }
    ]

    random_photo_set = random.choice(sample_photo_sets)

    message = ImageSendMessage(
        original_content_url=public_url + url_for('static', filename=f'album/{random_photo_set.get("original")}'),
        preview_image_url=public_url + url_for('static', filename=f'album/{random_photo_set.get("thumbnail")}')
    )

    return message
