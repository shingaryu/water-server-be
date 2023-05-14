from datetime import datetime

from linebot.models import FlexSendMessage

from common.message_templetes import event_flex_contents, select_event_message_contents
from common.mocks import mock_events

def select_entry_events_message():
    event_contents = []
    for event in mock_events:
        this_event_contents = event_flex_contents(datetime.fromisoformat(event["date"]), event["place"], 3,
                                                  f'select_event={event["_id"]["$oid"]}')
        event_contents += this_event_contents

    contents = select_event_message_contents(event_contents)
    flex_message = FlexSendMessage(
        alt_text='開催一覧',
        contents=contents
    )

    return flex_message
