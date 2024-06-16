import os
import ssl

from dotenv import load_dotenv

from create_rich_menu import create_rich_menu
from services.ngrok_service import connect_http_tunnel
from services.remind_service import REMIND_INTERVAL_MIN, REMIND_SOONER_THAN_HOURS, remind_closest_event
from set_webhook_url import set_webhook_url

load_dotenv()

from flask import Flask
from common.get_logger import get_logger
from common.line_bot_client import get_line_bot_client
from apscheduler.schedulers.background import BackgroundScheduler
from controllers.root_controller import root_bp
from controllers.linebot_controller import linebot_bp
from controllers.events_controller import events_bp
from controllers.movies_controller import movies_bp

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

port_to_serve = int(os.environ.get('PORT', 5000))  # 5000はflaskのデフォルトポート
logger.info(f'Flask application is to be served on port {port_to_serve}')
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッションを安全に使うための秘密鍵
app.register_blueprint(root_bp)
app.register_blueprint(linebot_bp)
app.register_blueprint(events_bp)
app.register_blueprint(movies_bp)

line_bot_api = get_line_bot_client()

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
scheduler.start()

if __name__ == '__main__':
    logger.info('開発サーバーモードでFlaskアプリケーションを起動します…')
    ssl._create_default_https_context = ssl._create_unverified_context
    public_url = connect_http_tunnel(port_to_serve)
    set_webhook_url(public_url)
    create_rich_menu()
    app.run(port=port_to_serve)
