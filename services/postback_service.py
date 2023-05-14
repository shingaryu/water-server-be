from datetime import datetime

from linebot.models import FlexSendMessage

from common.consts import SELECT_EVENT_TO_ENTRY, SELECT_EVENT_TO_ENTRY_EVENT
from templates.select_entry_events_template import event_flex_contents, select_event_message_contents
from common.mocks import mock_events
from templates.select_option_to_entry_template import select_option_to_entry_flex_contents

def select_entry_events_message():
    event_contents = []
    for event in mock_events:
        postback_data = f'{SELECT_EVENT_TO_ENTRY}/?{SELECT_EVENT_TO_ENTRY_EVENT}={event["_id"]["$oid"]}'
        this_event_contents = event_flex_contents(datetime.fromisoformat(event["startTime"]), event["place"], 3,
                                                  postback_data)
        event_contents += this_event_contents

    contents = select_event_message_contents(event_contents)
    flex_message = FlexSendMessage(
        alt_text='開催一覧',
        contents=contents
    )

    return flex_message

def select_option_to_entry_message(event_id):
    #todo: 動的にテンプレート生成
    contents = select_option_to_entry_flex_contents()
    flex_message = FlexSendMessage(
        alt_text='投票する',
        contents=contents
    )

    return flex_message

def entry_with_option():
    pass