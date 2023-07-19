# ngrokを立ち上げた状態でこのスクリプトを実行してください。
# ngrokは、環境変数PATHに設定されている場合、以下のコマンドで実行できます。
# ngrok http 5000

from dotenv import load_dotenv
load_dotenv()

import os
import requests
from common.get_logger import get_logger
from common.line_bot_client import get_line_bot_client

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

def set_webhook_url():
    line_bot_api = get_line_bot_client()

    # ngrokのAPIにアクセスしてpublic_urlを取得する
    response = requests.get("http://localhost:4040/api/tunnels")
    public_url = response.json()["tunnels"][0]["public_url"]

    # public_urlを標準出力に出力する
    logger.info(f'Public URL is: {public_url}')

    line_bot_api.set_webhook_endpoint(f'{public_url}/callback')
    logger.info(f'Set webhook URL to {public_url}/callback... done!')

if __name__ == '__main__':
    set_webhook_url()