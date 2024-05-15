import os
import ssl
import traceback
import calendar
from datetime import datetime

from bson import ObjectId
from dotenv import load_dotenv

from common.consts import SHOW_EVENTS, SELECT_EVENT_TO_ENTRY, SELECT_EVENT_TO_ENTRY_EVENT, \
    ENTRY_WITH_OPTION, ENTRY_WITH_OPTION_EVENT, ENTRY_WITH_OPTION_OPTION, SHOW_NEXT_EVENT, AKIO_BUTTON, SHOW_VIDEOS, SHOW_MEMBERS, \
    SHOW_VIDEOS_PLAYLIST
from common.utils import no_icon_image_public_url
from create_rich_menu import create_rich_menu
from repositories.mongo_repository import find_recent_events, insert_event, find_all_events, delete_event
from repositories.youtube_repository import refresh_token_if_expired, get_my_recent_videos
from services.ngrok_service import connect_http_tunnel
from services.postback_service import select_entry_events_message, select_option_to_entry_message, entry_with_option, \
    show_members_message, \
    show_recent_event_message, recent_videos, playlist_videos_message, get_or_default
from services.remind_service import REMIND_INTERVAL_MIN, REMIND_SOONER_THAN_HOURS, remind_closest_event
from set_webhook_url import set_webhook_url

load_dotenv()

from flask import Flask, request, render_template, session, redirect, url_for
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

port_to_serve = int(os.environ.get('PORT', 5000))  # 5000はflaskのデフォルトポート
logger.info(f'Flask application is to be served on port {port_to_serve}')
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッションを安全に使うための秘密鍵

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def show_events():
    events = find_recent_events(30)  # MongoDBから開催日のデータを取得
    return render_template('events.html', events=events)

def generate_dates(year, month, weekday):
    # 指定された年月のカレンダーを作成
    cal = calendar.monthcalendar(year, month)
    dates = []
    # カレンダーから指定された曜日の日付を抽出
    for week in cal:
        if week[weekday] != 0:  # calendar.monthcalendarは日付がない場合0を返す
            dates.append(datetime(year, month, week[weekday]))
    return dates

@app.route('/events/register', methods=['GET', 'POST'])
def events_register():
    if request.method == 'POST': # ボタンクリック時
        # ユーザーの入力状態をsessionに保存
        session['location'] = request.form.get('location', '◯◯体育館')
        session['selected_year'] = int(request.form.get('selected_year', datetime.now().year))
        session['selected_month'] = int(request.form.get('selected_month', (datetime.now().month % 12) + 1))
        session['selected_dayofweek'] = int(request.form.get('dayOfWeek', 6))
        # session['dates'] = request.form.get({}) # ユーザー入力で変更されないので不要
        session['start_hour'] = int(request.form['start_hour'])
        session['start_minute'] = int(request.form['start_minute'])
        session['end_hour'] = int(request.form['end_hour'])
        session['end_minute'] = int(request.form['end_minute'])

        selected_dates = request.form.getlist('selected_dates') # sessionに保存せず、送信してリロードしたら自然に消去

        if 'apply_button' in request.form:  # 選択した開催日を登録 クリック
            for date_str in selected_dates:
                location = session.get('location', '◯◯体育館')
                start_hour = session.get('start_hour', 0)
                start_minute = session.get('start_minute', 0)
                end_hour = session.get('end_hour', 0)
                end_minute = session.get('end_minute', 0)

                # 日時オブジェクトの作成
                start_time = datetime.strptime(f"{date_str} {start_hour}:{start_minute}", "%Y-%m-%d %H:%M")
                end_time = datetime.strptime(f"{date_str} {end_hour}:{end_minute}", "%Y-%m-%d %H:%M")

                # MongoDBドキュメントの作成
                event_document = {
                    "startTime": start_time,
                    "endTime": end_time,
                    "place": location,
                    "entryOptions": [
                        {"id": "1", "text": "参加"},
                        {"id": "2", "text": "途中参加"},
                        {"id": "3", "text": "不参加"}
                    ]
                }
                insert_event(event_document)
            session['selected_dayofweek'] = 6
            session['dates'] = [date.strftime('%Y-%m-%d') for date in generate_dates(session['selected_year'], session['selected_month'], 6)]
            return redirect(url_for('events_register'))
        else: # 年、月、曜日ドロップダウンの選択状態変更
            session['dates'] = [date.strftime('%Y-%m-%d') for date in generate_dates(session['selected_year'], session['selected_month'], session['selected_dayofweek'])]
            return redirect(url_for('events_register')) # -> GETリクエストへ

    # GETリクエスト(ページ読み込み時)
    return render_template('events_register.html',
        place=session.get('location', '◯◯体育館'),
        selected_year=session.get('selected_year', datetime.now().year),
        selected_month = session.get('selected_month', (datetime.now().month % 12) + 1),
        selected_dayofweek = session.get('selected_dayofweek', 6),
        dates=session.get('dates', [date.strftime('%Y-%m-%d') for date in generate_dates(datetime.now().year, (datetime.now().month % 12) + 1, 6)]),
        start_hour=session.get('start_hour', 9),
        start_minute=session.get('start_minute', 0),
        end_hour=session.get('end_hour', 12),
        end_minute=session.get('end_minute', 0),
    )

@app.route('/events/delete', methods=['GET', 'POST'])
def events_delete():
    if request.method == 'POST':
        if 'delete_event' in request.form:
            event_id = request.form['delete_event']
            delete_event(ObjectId(event_id))
            return redirect(url_for('events_delete'))

    events = find_all_events(ascending=True)
    return render_template('events_delete.html', events=events)

@app.route('/movies')
def show_movies():
    youtube_videos = get_my_recent_videos()

    videos = []
    for video in youtube_videos:
        thumbnail_image_url = get_or_default(video, lambda x: x.get("snippet").get("thumbnails").get("high").get("url"), no_icon_image_public_url())
        title = get_or_default(video, lambda x: x.get("snippet").get("title")[:40], " ")
        text = get_or_default(video, lambda x: x.get("snippet").get("description")[:60], " ")
        video_id = get_or_default(video, lambda x: x.get('id').get('videoId'), 'error')
        videos.append({ "thumbnail": thumbnail_image_url, "title": title, "description": text, "id": video_id})
    return render_template('movies.html', videos=videos)

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
            flex_messages:list = show_members_message()
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

if __name__ == '__main__':
    logger.info('開発サーバーモードでFlaskアプリケーションを起動します…')
    ssl._create_default_https_context = ssl._create_unverified_context
    public_url = connect_http_tunnel(port_to_serve)
    set_webhook_url(public_url)
    create_rich_menu()
    app.run(port=port_to_serve)
