import os
from linebot.models import FlexSendMessage, TextSendMessage, CarouselTemplate, CarouselColumn, URIAction, \
    TemplateSendMessage, QuickReply, QuickReplyButton, PostbackAction

from common.consts import SELECT_EVENT_TO_ENTRY, SELECT_EVENT_TO_ENTRY_EVENT, SHOW_VIDEOS, SHOW_VIDEOS_PLAYLIST
from common.get_logger import get_logger
from common.utils import no_icon_image_public_url
from repositories.youtube_repository import get_my_recent_videos, get_playlist_videos, get_my_playlists
from repositories.mongo_repository import find_recent_events, find_all_events, find_all_entries, find_event, find_entry, \
    insert_entry, delete_entry, generate_member_info_dict, MemberInfo
from line_message_templates.select_entry_events_template import event_flex_contents, select_event_message_contents
from line_message_templates.select_option_to_entry_template import select_option_to_entry_flex_contents
from line_message_templates.show_members_template import member_contents, member_list_bubble

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

N_RECENT_EVENTS = 5

def show_recent_event_message():
    events = find_recent_events(1)
    if len(events) == 0:
        return TextSendMessage(text='直近の開催予定がありません。')
    else:
        return select_option_to_entry_message(events[0]["_id"])

def show_members_message() -> list[FlexSendMessage]:       
    members_info: dict[str, MemberInfo] = generate_member_info_dict(find_all_events())

    #TODO Calculate the appearance (Appearance/The total events)
    #TODO Check if users are coming to the next event.　(Y/N)
    #TODO sort the user list by attendance to the next event. The absentees come first.
    
    sorted_members_info = dict(sorted(members_info.items(), key=lambda item: (item[1].firstEntryDateTime, item[1].displayName)))

    #Generate flex send messages
    flex_messages = []   
    users_flex_contents = []
    count: int = 0
    # Find out how many lists we need before generating flex messages.
    max_count_in_a_bubble: int = 30 #This is just a random number. you can change whatever you want.
    member_list_num: int = len(sorted_members_info) // max_count_in_a_bubble
    if len(sorted_members_info) % max_count_in_a_bubble != 0:
        member_list_num += 1
    member_list_count: int = 0

    max_attendance: int = max([member_info.totalAttendance for member_info in sorted_members_info.values()])

    for member_info in sorted_members_info.values():
        count += 1
        name: str = member_info.displayName
        image_url: str = member_info.pictureUrl
        total_attendance: str = str(member_info.totalAttendance)
        user_flex_contents: dict = member_contents(name, image_url, total_attendance, float(total_attendance) / max_attendance)
        users_flex_contents.append(user_flex_contents)

        if member_list_num == 1:
            if (count == len(sorted_members_info)):
                contents = member_list_bubble('メンバーリスト', users_flex_contents)
                flex_message = FlexSendMessage(
                    alt_text='メンバー一覧',
                    contents=contents
                )
                flex_messages.append(flex_message)
        else:
            if (count % max_count_in_a_bubble == 0) or (count == len(sorted_members_info)):
                member_list_count += 1
                contents = member_list_bubble('メンバーリスト' +" (%s)" % (str(member_list_count) + "/" + str(member_list_num)), users_flex_contents)
                flex_message = FlexSendMessage(
                    alt_text='メンバー一覧',
                    contents=contents
                )
                flex_messages.append(flex_message)
                users_flex_contents.clear()
    
    return flex_messages

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


def videos_quick_reply_obj():
    playlists = get_my_playlists()[:12]  # maximum items in quick reply: 13
    items = [
        QuickReplyButton(
            action=PostbackAction(label="全部", data=f"{SHOW_VIDEOS}")
        )
    ]

    items.extend([
            QuickReplyButton(
            image_url=playlist.get("snippet").get("thumbnails").get("default").get("url"),
            action=PostbackAction(
                label=playlist.get("snippet").get("title"),
                data=f"{SHOW_VIDEOS}/?{SHOW_VIDEOS_PLAYLIST}={playlist.get('id')}"),
                display_text=playlist.get("snippet").get("title"),
            ) for playlist in playlists
    ])

    return QuickReply(items=items)


def get_or_default(video, func, default):
    try:
        res = func(video)
        return res or default
    except Exception as e:
        logger.warn(f"failed to get attribute of the video. setting default value...")
        return default


def recent_videos():
    videos = get_my_recent_videos()[:10]

    columns = []
    for video in videos:
        thumbnail_image_url = get_or_default(video, lambda x: x.get("snippet").get("thumbnails").get("high").get("url"), no_icon_image_public_url())
        title = get_or_default(video, lambda x: x.get("snippet").get("title")[:40], " ")
        text = get_or_default(video, lambda x: x.get("snippet").get("description")[:60], " ")  # required
        action = URIAction(label="見る", uri=f"https://www.youtube.com/watch?v={get_or_default(video, lambda x: x.get('id').get('videoId'), 'error')}")  # required

        columns.append(CarouselColumn(
            thumbnail_image_url=thumbnail_image_url,
            title=title,
            text=text,
            default_action=action,
            actions=[action]
        ))

    template = CarouselTemplate(columns=columns)

    message = TemplateSendMessage(alt_text="動画一覧", template=template, quick_reply=videos_quick_reply_obj())

    return message


def playlist_videos_message(playlist_id: str):
    videos = get_playlist_videos(playlist_id)[:10]

    columns = []
    for video in videos:
        thumbnail_image_url = get_or_default(video, lambda x: x.get("snippet").get("thumbnails").get("high").get("url"), no_icon_image_public_url())
        title = get_or_default(video, lambda x: x.get("snippet").get("title")[:40], " ")
        text = get_or_default(video, lambda x: x.get("snippet").get("description")[:60], " ")  # required
        action = URIAction(label="見る", uri=f"https://www.youtube.com/watch?v={get_or_default(video, lambda x: x.get('snippet').get('resourceId').get('videoId'), 'error')}")  # required, ここだけrecent_videosと異なる

        columns.append(CarouselColumn(
            thumbnail_image_url=thumbnail_image_url,
            title=title,
            text=text,
            default_action=action,
            actions=[action]
        ))

    template = CarouselTemplate(columns=columns)

    message = TemplateSendMessage(alt_text="動画一覧", template=template, quick_reply=videos_quick_reply_obj())

    return message
