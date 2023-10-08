import os

from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage
from pymongo.errors import PyMongoError

from common.get_logger import get_logger
from repositories.mongo_repository import find_recent_events
from repositories.mongo_repository import update_event
from datetime import datetime, timedelta

from services.postback_service import show_recent_event_message

REMIND_INTERVAL_MIN = 60
REMIND_SOONER_THAN_HOURS = 24

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))


# 指定した時間差time_differenceがh時間m分s秒以内か判断するプログラム
def is_over_n_hours(time_difference, h, m, s):
    time_hms = timedelta(hours=h, minutes=m, seconds=s)
    return time_difference <= time_hms


# REMIND_INTERVAL_MIN分ごとに実行するプログラムの中身
def remind_closest_event(line_bot_api):
    logger.info(f'{REMIND_INTERVAL_MIN}分ごとに実行されるプログラム')

    # 直近のイベントメッセージを取得
    message = show_recent_event_message()
    # 直近のイベントの時刻情報を取得し、現在時刻との時間差を求める
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

    # 直近のイベントのリマインド済みフラグ情報を取得
    isRemindedFlag = results[0].get('isReminded', False)
    logger.debug(f'リマインド済み: {isRemindedFlag}')

    # 直近のイベント時刻までの時間がREMIND_SOONER_THAN_HOURS時間以内且つリマインド済みでない場合にメッセージと投票状況を送信
    if is_over_n_hours(delta_time, REMIND_SOONER_THAN_HOURS, 0, 0) and not isRemindedFlag:
        try:
            # (a)メッセージ送信 -> (b)MongoDBへの保存 の順番だと、(b)だけ失敗する状況でメッセージが送られ続けてしまうので、(b) -> (a)の順番にしておく
            # イベントにリマインド済みフラグを設定
            logger.debug('イベントにリマインド済みフラグを設定...')
            oid = results[0]['_id']
            field_to_update = {'isReminded': True}
            update_event(oid, field_to_update)

            text_message = TextSendMessage(text='【自動配信】次回の開催まであと1日です。参加状況を連絡します。投票がまだの方は投票してください。')
            messages = [text_message, message]
            line_bot_api.broadcast(messages=messages)
            logger.info('メッセージを送信しました')
        except PyMongoError as e:
            logger.error("DBへの保存に失敗しました:", e)
        except LineBotApiError as e:
            logger.error('メッセージの送信に失敗しました:', e)