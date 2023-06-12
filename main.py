from bson import ObjectId
from dotenv import load_dotenv
from pymongo.errors import PyMongoError

from common.consts import SHOW_EVENTS, SELECT_EVENT_TO_ENTRY, SELECT_EVENT_TO_ENTRY_EVENT, \
    ENTRY_WITH_OPTION, ENTRY_WITH_OPTION_EVENT, ENTRY_WITH_OPTION_OPTION, SHOW_NEXT_EVENT, AKIO_BUTTON
from services.postback_service import select_entry_events_message, select_option_to_entry_message, entry_with_option, \
    show_recent_event_message

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
from urllib.parse import parse_qs, urlparse

from repositories.mongo_repository import find_recent_events
from repositories.mongo_repository import update_event
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

app = Flask(__name__)

scheduler = BackgroundScheduler(daemon=True)

line_bot_api = get_line_bot_client()
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET', None))

REMIND_INTERVAL_MIN = 20
REMIND_SOONER_THAN_HOURS = 24

#指定した時間差time_differenceがh時間m分s秒以内か判断するプログラム
def is_over_n_hours(time_difference, h, m, s):
    time_hms = timedelta(hours=h, minutes=m, seconds=s)
    return time_difference <= time_hms

#REMIND_INTERVAL_MIN分ごとに実行するプログラムの中身
def remind_closest_event():
    logger.info(f'{REMIND_INTERVAL_MIN}分ごとに実行されるプログラム')

    #直近のイベントメッセージを取得
    message = show_recent_event_message()
    #直近のイベントの時刻情報を取得し、現在時刻との時間差を求める
    results = find_recent_events(1)
    if len(results) == 0:
        logger.info('開催予定のイベントはありません。')
        return
    
    recent_time = results[0]["startTime"]
    current_time = datetime.now()
    delta_time = recent_time - current_time
    logger.debug(f'現在時刻: {current_time}')
    logger.debug(f'イベント時刻: {recent_time}')
    logger.debug(f'イベント時刻まであと: {delta_time}')

    #直近のイベントのリマインド済みフラグ情報を取得
    isRemindedFlag = results[0].get('isReminded', False)
    #直近のイベント時刻までの時間がREMIND_SOONER_THAN_HOURS時間以内且つリマインド済みでない場合にメッセージと投票状況を送信
    if is_over_n_hours(delta_time,REMIND_SOONER_THAN_HOURS,0,0) and not isRemindedFlag:
        try:
            #(a)メッセージ送信 -> (b)MongoDBへの保存 の順番だと、(b)だけ失敗する状況でメッセージが送られ続けてしまうので、(b) -> (a)の順番にしておく
            #イベントにリマインド済みフラグを設定
            logger.debug('イベントにリマインド済みフラグを設定...')
            oid = results[0]['_id']
            field_to_update = {'isReminded': True}
            update_event(oid, field_to_update)

            text_message = TextSendMessage(text='【自動配信】次回の開催まであと1日です。参加状況を連絡します。投票がまだの方は投票してください。')
            messages = [text_message, message]
            line_bot_api.broadcast(messages = messages)
            logger.info('メッセージを送信しました')
        except PyMongoError as e:
            logger.error("DBへの保存に失敗しました:", e)
        except LineBotApiError as e:
            logger.error('メッセージの送信に失敗しました:', e)

#REMIND_INTERVAL_MIN分ごとにremind_closest_eventを実行するよう指示
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(remind_closest_event, 'interval', minutes=REMIND_INTERVAL_MIN)
    scheduler.start()

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
    # except Exception as e:
    #     logger.error(f'Got internal exception: {e.message}')

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
    try:
        parsed_url = urlparse(line_event.postback.data)
        query_params = parse_qs(parsed_url.query)
        event_name = parsed_url.path.strip("/")
        if (event_name == SHOW_NEXT_EVENT):
            message = show_recent_event_message()
            line_bot_api.reply_message(line_event.reply_token, message)
        elif (event_name == SHOW_EVENTS):
            message = select_entry_events_message()
            line_bot_api.reply_message(line_event.reply_token, message)
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
        elif (event_name == AKIO_BUTTON):
            message = TextSendMessage(text='こんにちは、林亮夫です。')
            line_bot_api.reply_message(line_event.reply_token, message)
        else:
            line_bot_api.reply_message(
                line_event.reply_token,
                TextSendMessage(text='まだ実装してないよ。ごめんね！！'))
    except Exception as e:
        line_bot_api.reply_message(
            line_event.reply_token,
            TextSendMessage(text=f'サーバー内部でエラーが発生しました。\n{str(e)}'))
        raise e

if __name__ == '__main__':
    print('line-api-use-case-flask:main')
    start_scheduler()
    app.run()
