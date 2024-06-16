import os
import traceback
from urllib.parse import urlparse, parse_qs

from bson import ObjectId
from flask import Blueprint, request
from linebot import WebhookHandler
from linebot.models import MessageEvent, PostbackEvent, TextMessage, TextSendMessage
from linebot.exceptions import LineBotApiError, InvalidSignatureError
from common.get_logger import get_logger
from common.line_bot_client import get_line_bot_client
from services.postback_service import select_entry_events_message, select_option_to_entry_message, entry_with_option, show_members_message, show_recent_event_message, recent_videos, playlist_videos_message, get_or_default
from common.consts import SHOW_EVENTS, SELECT_EVENT_TO_ENTRY, SELECT_EVENT_TO_ENTRY_EVENT, ENTRY_WITH_OPTION, ENTRY_WITH_OPTION_EVENT, ENTRY_WITH_OPTION_OPTION, SHOW_NEXT_EVENT, AKIO_BUTTON, SHOW_VIDEOS, SHOW_MEMBERS, SHOW_VIDEOS_PLAYLIST

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

linebot_bp = Blueprint('linebot', __name__)

line_bot_api = get_line_bot_client()
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET', None))

@linebot_bp.route("/callback", methods=['POST'])
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

@handler.add(MessageEvent, message=TextMessage)
def text_message(line_event):
    text = line_event.message.text
    line_bot_api.reply_message(line_event.reply_token, TextSendMessage(text=text))

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
            flex_messages = show_members_message()
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
            playlist_id = query_params.get(SHOW_VIDEOS_PLAYLIST)[0] if query_params.get(SHOW_VIDEOS_PLAYLIST) else None
            if playlist_id is not None:
                message = playlist_videos_message(playlist_id)
            else:
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
