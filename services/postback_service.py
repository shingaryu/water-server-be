import os
from bson import ObjectId
from linebot.models import FlexSendMessage, TextSendMessage, CarouselTemplate, CarouselColumn, URIAction, \
    TemplateSendMessage

from common.consts import SELECT_EVENT_TO_ENTRY, SELECT_EVENT_TO_ENTRY_EVENT
from common.get_logger import get_logger
from repositories.youtube_repository import get_my_recent_videos
from repositories.mongo_repository import find_recent_events, find_all_events, find_all_entries, find_event, find_entry, \
    insert_entry, delete_entry, find_all_members_in_the_event
from templates.select_entry_events_template import event_flex_contents, select_event_message_contents
from templates.select_option_to_entry_template import select_option_to_entry_flex_contents
from templates.show_members_template import member_contents_demo

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

N_RECENT_EVENTS = 5

def show_recent_event_message():
    events = find_recent_events(1)
    if len(events) == 0:
        return TextSendMessage(text='直近の開催予定がありません。')
    else:
        return select_option_to_entry_message(events[0]["_id"])

def show_members_attending_the_recent_event_in_text_message() -> TextSendMessage:
    #Find the next event
    events: list = find_recent_events(1)
    if len(events) != 1:
        logger.error("Couldn't find the next event!")
        return TextSendMessage("Couldn't find the next event!")
    event_id: ObjectId = events[0]["_id"]

    #Find members who are going to the next event
    users: dict = find_all_members_in_the_event(event_id)

    #Generate a flex message
    text:str = str()
    i: int = 0
    for user in users.values():
        i += 1
        text += user["displayName"]
        if (i != len(users)):
            text += "\n"

    return TextSendMessage(text=text)

def show_members_attending_the_recent_event_in_flex_message() ->FlexSendMessage:
    #Find the next event
    events: list = find_recent_events(1)
    if len(events) != 1:
        logger.error("Couldn't find the next event!")
        return TextSendMessage("Couldn't find the next event!")
    event_id: ObjectId = events[0]["_id"]

    #Find members who are going to the next event
    users: dict = find_all_members_in_the_event(event_id)

    #Generate a flex send message
    users_flex_contents = []
    for user in users.values():
        name: str = user["displayName"]
        image_url: str = user["pictureUrl"]
        user_flex_contents: dict = member_contents(name, image_url)
        users_flex_contents.append(user_flex_contents)

    contents = {
        "type": "carousel",
        "contents": users_flex_contents
    }

    flex_message = FlexSendMessage(
        alt_text='メンバ一覧',
        contents=contents
    )
    return flex_message

def show_members_message_demo() -> list[FlexSendMessage]:

    #This is for all events.
    events: list = find_all_events()
    event_ids: set = {ObjectId}
    for event in events:
        event_ids.add(event["_id"])

    users = {}
    for event_id in list(event_ids):
        users = users | find_all_members_in_the_event(event_id)

    #Sort by name... Tried.. but seems not sorted by name. why??
    sorted_users = dict(sorted(users.items(), key=lambda item: item[1]["displayName"]))

    #Generate flex send messages
    flex_messages = []   
    users_flex_contents = []
    count: int = 0
    for user in sorted_users.values():
        count += 1
        name: str = user["displayName"]
        image_url: str = user["pictureUrl"]
        user_flex_contents: dict = member_contents_demo(name, image_url)
        users_flex_contents.append(user_flex_contents)

        #One carousel message type can have up to 12 items. If there are more users, need to break a message into multiple messages.
        if (count % 12 == 0) or (count == len(users)):
            contents = {
                "type": "carousel",
                "contents": users_flex_contents
            }

            flex_message = FlexSendMessage(
                alt_text='メンバ一覧',
                contents=contents
            )

            flex_messages.append(flex_message)
            users_flex_contents.clear()
    
    return flex_messages

def show_members_message() -> FlexSendMessage:
    #This is for all events.
    events: list = find_all_events()
    event_ids: set = {ObjectId}
    for event in events:
        event_ids.add(event["_id"])

    users = {}
    for event_id in list(event_ids):
        users = users | find_all_members_in_the_event(event_id)

    #Sort by name... Tried.. but seems not sorted by name. why??
    sorted_users = dict(sorted(users.items(), key=lambda item: item[1]["displayName"]))

    #Generate flex send messages
    flex_messages = []   
    users_flex_contents = []
    count: int = 0
    return FlexSendMessage

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

def recent_videos():
    videos = get_my_recent_videos()[:10]

    template = CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url=video.get("snippet").get("thumbnails").get("high").get("url"),
                title=video.get("snippet").get("title")[:40] or " ", # 最大40文字(Messaging API制限)、must be non-empty text
                text=video.get("snippet").get("description")[:60] or " ", # 最大60文字(Messaging API制限)、must be non-empty text
                default_action=URIAction(label="見る", uri=f"https://www.youtube.com/watch?v={video.get('id').get('videoId')}"),
                actions=[
                    URIAction(label="見る", uri=f"https://www.youtube.com/watch?v={video.get('id').get('videoId')}")
                ]
            ) for video in videos
        ]
    )

    message = TemplateSendMessage(alt_text="動画一覧", template=template)

    return message