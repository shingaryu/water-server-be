from dotenv import load_dotenv

from services.postback_service import select_entry_events_message

load_dotenv()

import os
import json

from flask import Flask, request
from linebot import WebhookHandler
from linebot.models import (
    MessageEvent, PostbackEvent, TextMessage,
    TextSendMessage
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from common import utils
from common.get_logger import get_logger
from common.line_bot_client import get_line_bot_client

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

app = Flask(__name__)

line_bot_api = get_line_bot_client()
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET', None))

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
    postback_data = line_event.postback.data.split('=')
    if (postback_data[0] == 'area' and postback_data[1] == '0'):
        logger.debug('area 0 clicked')
        message = select_entry_events_message()
        line_bot_api.reply_message(line_event.reply_token, message)

if __name__ == '__main__':
    print('line-api-use-case-flask:main')
    app.run()
