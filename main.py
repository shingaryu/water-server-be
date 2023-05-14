from dotenv import load_dotenv
load_dotenv()

import os
import json
import datetime

from flask import Flask, request
from linebot import WebhookHandler
from linebot.models import (
    MessageEvent, PostbackEvent, TextMessage,
    TextSendMessage, FlexSendMessage
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from common import utils
from common.get_logger import get_logger
from common.line_bot_client import get_line_bot_client
from common.message_templetes import select_event_message_contents, event_flex_contents

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

app = Flask(__name__)

line_bot_api = get_line_bot_client()
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET', None))

mock_events = [
    {
        "_id": {
            "ObjectId": "6456313426165d3c40069c2f"
        },
        "date": "2023-05-12T18:00:00+09:00",
        "place": "志村第五小学校"
    },
    {
        "_id": {
            "ObjectId": "6456318526165d3c40069c30"
        },
        "date": "2023-05-14T09:00:00+09:00",
        "place": "桜台体育館"
    }
]

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/callback", methods=['POST'])
def request_handler():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    logger.info("Request body: " + body)

    error_json = utils.create_error_response('Error')
    error_json['isBase64Encoded'] = False

    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        logger.error('Got exception from LINE Messaging API: %s\n' % e.message)
        for m in e.error.details:
            logger.error('  %s: %s' % (m.property, m.message))
        return error_json
    except InvalidSignatureError as e:
        logger.error('Got exception from LINE Messaging API: %s\n' % e.message)
        return error_json
    else:
        ok_json = utils.create_success_response(
            json.dumps('Success'))
        ok_json['isBase64Encoded'] = False
        return ok_json

# オウム返し。現状は死活確認用
@handler.add(MessageEvent, message=TextMessage)
def text_message(line_event):
    text = line_event.message.text
    line_bot_api.reply_message(
        line_event.reply_token,
        TextSendMessage(text=text))

@handler.add(PostbackEvent)
def postback(line_event):
    postback_data = line_event.postback.data
    if (postback_data.split('=')[0] == 'area'):
        if (postback_data.split('=')[1] == '0'):
            logger.debug('area 0 clicked')

            event_contents = []
            for event in mock_events:
                date = event["date"]
                this_event_contents = event_flex_contents(datetime.datetime.fromisoformat(event["date"]), event["place"], 3, f'select_event={event["_id"]["ObjectId"]}')
                event_contents += this_event_contents

            contents = select_event_message_contents(event_contents)
            flex_message = FlexSendMessage(
                alt_text='開催一覧',
                contents=contents
            )

            line_bot_api.reply_message(line_event.reply_token, flex_message)

if __name__ == '__main__':
    print('line-api-use-case-flask:main')
    app.run()
