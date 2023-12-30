import os
import ssl
import traceback

from bson import ObjectId
from dotenv import load_dotenv
from pyngrok import ngrok

from common.consts import SHOW_EVENTS, SELECT_EVENT_TO_ENTRY, SELECT_EVENT_TO_ENTRY_EVENT, \
    ENTRY_WITH_OPTION, ENTRY_WITH_OPTION_EVENT, ENTRY_WITH_OPTION_OPTION, SHOW_NEXT_EVENT, AKIO_BUTTON, SHOW_VIDEOS, SHOW_MEMBERS
from repositories.youtube_repository import refresh_token_if_expired
from services.postback_service import select_entry_events_message, select_option_to_entry_message, entry_with_option, show_members_message_demo, show_members_message,\
    show_recent_event_message, recent_videos, show_members_attending_the_recent_event_in_text_message
from services.remind_service import REMIND_INTERVAL_MIN, REMIND_SOONER_THAN_HOURS, remind_closest_event
from set_webhook_url import set_webhook_url

load_dotenv()

from flask import Flask, request
from linebot import WebhookHandler
from linebot.models import (
    MessageEvent, PostbackEvent, TextMessage,
    TextSendMessage
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from common.get_logger import get_logger
from common.line_bot_client import get_line_bot_client
from urllib.parse import parse_qs, urlparse
from apscheduler.schedulers.background import BackgroundScheduler

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

app = Flask(__name__)
line_bot_api = get_line_bot_client()
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET', None))

REFRESH_TOKEN_INTERVAL_MIN = 60 * 12

# Todo: このバックグラウンドジョブが本当に必要かどうか調査
def refresh_googleapi_token():
    logger.info("Google API トークンの有効期限を確認しています…")
    refresh_token_if_expired()

# REMIND_INTERVAL_MIN分ごとにremind_closest_eventを実行するよう指示
scheduler = BackgroundScheduler(daemon=True)  # background thread
logger.info('schedulerジョブを設定します...')
logger.debug(f'REMIND_INTERVAL_MIN: {REMIND_INTERVAL_MIN}')
logger.debug(f'REMIND_SOONER_THAN_HOURS: {REMIND_SOONER_THAN_HOURS}')
scheduler.add_job(
    func=remind_closest_event,
    trigger='interval',
    args=[line_bot_api],
    minutes=REMIND_INTERVAL_MIN
)
scheduler.add_job(
    func=refresh_googleapi_token,
    trigger='interval',
    minutes=REFRESH_TOKEN_INTERVAL_MIN
)
scheduler.start()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/callback", methods=['POST'])
def request_handler():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        logger.error('Signature invalid. You are using wrong channel secret or this is unauthorized request: %s\n' % e.message)
        traceback.print_exc()
    except LineBotApiError as e:
        logger.error('Got exception from LINE Messaging API: %s\n' % e.message)
        for m in e.error.details:
            logger.error('  %s: %s' % (m.property, m.message))
        traceback.print_exc()
    except Exception as e:
        logger.error(f'Got internal exception: {e}')
        traceback.print_exc()

    return 'OK'

def reply_to_user_on_error(reply_token):
    logger.debug("固定のエラーメッセージをユーザーに送信します…")
    try:
        line_bot_api.reply_message(reply_token, TextSendMessage(text='サーバーエラーにより、うまく処理できませんでした。ごめんね！！'))
    except Exception:  # 他の例外発生時の使用を想定しているため、本関数内での例外は無視
        logger.warning('エラーメッセージの送信に失敗しました。元の処理を続行します…')

# オウム返し。現状は死活確認用
@handler.add(MessageEvent, message=TextMessage)
def text_message(line_event):
    text = line_event.message.text
    line_bot_api.reply_message(
        line_event.reply_token,
        TextSendMessage(text=text))

@handler.add(PostbackEvent)
def postback(line_event):
    try:
        parsed_url = urlparse(line_event.postback.data)
        query_params = parse_qs(parsed_url.query)
        event_name = parsed_url.path.strip("/")
    except Exception as e:
        logger.error(f'postbackデータのparseに失敗しました。{line_event.postback.data}')
        reply_to_user_on_error(line_event.reply_token)
        raise e

    try:
        if (event_name == SHOW_NEXT_EVENT):
            message = show_recent_event_message()
            line_bot_api.reply_message(line_event.reply_token, message)
        elif (event_name == SHOW_EVENTS):
            message = select_entry_events_message()
            line_bot_api.reply_message(line_event.reply_token, message)
        elif (event_name == SHOW_MEMBERS):
            #TODO: Return user list here and check the number of users, if it's grater than 12. Send the flex message multiple times.
            flex_messages:list = show_members_message()
            # for message in flex_messages:
            line_bot_api.reply_message(line_event.reply_token, flex_messages)
        elif (event_name == SELECT_EVENT_TO_ENTRY):
            event_id = query_params.get(SELECT_EVENT_TO_ENTRY_EVENT)[0]
            message = select_option_to_entry_message(ObjectId(event_id))
            line_bot_api.reply_message(line_event.reply_token, message)
        elif (event_name == ENTRY_WITH_OPTION):
            event_id = query_params.get(ENTRY_WITH_OPTION_EVENT)[0]
            option_id = query_params.get(ENTRY_WITH_OPTION_OPTION)[0]
            profile = line_bot_api.get_profile(line_event.source.user_id)
            message = entry_with_option(event_id, option_id, profile)
            line_bot_api.reply_message(line_event.reply_token, message)
        elif (event_name == SHOW_VIDEOS):
            message = recent_videos()
            line_bot_api.reply_message(line_event.reply_token, message)
        elif (event_name == AKIO_BUTTON):
            message = TextSendMessage(text='こんにちは、林亮夫です。')
            line_bot_api.reply_message(line_event.reply_token, message)
        else:
            line_bot_api.reply_message(
                line_event.reply_token,
                TextSendMessage(text='まだ実装してないよ。ごめんね！！'))
    except Exception as e:
        logger.error(f'postbackイベントの処理に失敗しました。event: {event_name}, params: {query_params}')
        reply_to_user_on_error(line_event.reply_token)
        raise e

if __name__ == '__main__':
    logger.info('開発サーバーモードでFlaskアプリケーションを起動します…')
    ssl._create_default_https_context = ssl._create_unverified_context
    http_tunnel = ngrok.connect("5000", "http")
    set_webhook_url(http_tunnel.public_url)
    app.run()
