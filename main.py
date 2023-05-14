from dotenv import load_dotenv
load_dotenv()

import os
import json
import datetime

from flask import Flask, request
from linebot import WebhookHandler
from linebot.models import (
    MessageEvent, PostbackEvent, FollowEvent, TextMessage, ImageMessage,
    TextSendMessage, FlexSendMessage, QuickReply, TemplateSendMessage,
    ConfirmTemplate, ButtonsTemplate
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from common import (common_const, utils)
from common.get_logger import get_logger
from common.line_bot_client import get_line_bot_client
from common.message_templetes import select_event_message_contents, event_flex_contents

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

app = Flask(__name__)

line_bot_api = get_line_bot_client()
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET', None))

def get_sigunature(key_search_dict):
    """
    署名発行に必要なx-line-signatureを大文字小文字区別せずに取得し、署名内容を返却する

    Parameters
    ----------
    key_search_dict : dict
        Webhookへのリクエストのheaders

    Returns
    -------
    signature : str
        LINE Botの署名
    """
    for key in key_search_dict.keys():
        if key.lower() == 'x-line-signature':
            signature = key_search_dict[key]
            return signature


def convert_user_id(event):
    """
    LINE UserIdのマスク処理

    Parameters
    ----------
    event : dict
        Webhookへのリクエスト内容。

    Returns
    -------
    log_event : dict
        UserIdマスク後のリクエスト内容。
    """
    log_body = json.loads(event['body'])
    update_body = []
    for linebot_event in log_body['events']:
        linebot_event['source']['userId'] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        update_body.append(linebot_event)
    del log_body['events']
    log_body['events'] = update_body
    log_event = event
    log_event['body'] = json.dumps(log_body, ensure_ascii=False)

    return log_event

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/callback", methods=['POST'])
def request_handler():
    """
    Webhookに送信されたLINEトーク内容を返却する

    Returns
    -------
    Response : dict
        Webhookへのレスポンス内容。
    """

    signature = request.headers['X-Line-Signature']
    # signature = get_sigunature(event['headers'])

    # log_event = event.copy()
    # logger.info(convert_user_id(log_event))

    # body = event['body']
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

    # データを貯めるなどの処理を実施したい場合は、SQSなどにメッセージ通知をして、それをトリガーに別途Lambdaを起動して処理する


@handler.add(MessageEvent, message=TextMessage)
def text_message(line_event):
    """
    Webhookに送信されたLINEメッセージ(テキスト)イベントについて処理を実施する

    Parameters
    ----------
    line_event : dict
        LINEメッセージイベント内容。

    """
    text = line_event.message.text
    line_bot_api.reply_message(
        line_event.reply_token,
        TextSendMessage(text=text))


@handler.add(MessageEvent, message=ImageMessage)
def image_message(line_event):
    """
    Webhookに送信されたLINEメッセージイベント(画像)について処理を実施する

    Parameters
    ----------
    line_event: dict
        LINEメッセージイベント内容。

    """
    line_bot_api.reply_message(
        line_event.reply_token,
        TextSendMessage(text='画像を受け付けました(画像は保存されません)'))


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

@handler.add(PostbackEvent)
def postback(line_event):
    """
    Webhookに送信されたLINEポストバックイベントについて処理を実施する

    Parameters
    ----------
    line_event: dict
        LINEメッセージイベント内容。

    """

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
