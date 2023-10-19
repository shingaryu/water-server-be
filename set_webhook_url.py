# ngrokで発行したpublic URLをLINE messaging APIのwebhook URLに設定します。
# ngrokは開発サーバー(main関数)とプロダクション環境では異なる起動方法を想定しています。
# 開発サーバーではpyngrokライブラリを用いてPythonプログラム内でngrokを起動します。
# プロダクション環境ではPythonプログラムとは別プロセスで、既にngrokが起動していることを前提とします。

from dotenv import load_dotenv
load_dotenv()

import os
import requests
from common.get_logger import get_logger
from common.line_bot_client import get_line_bot_client

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))


def set_webhook_url(public_url):
    line_bot_api = get_line_bot_client()
    line_bot_api.set_webhook_endpoint(f'{public_url}/callback')
    logger.info(f'Set webhook URL to {public_url}/callback... done!')


# 既に立ち上がっているngrokインスタンスのpublic_urlを取得する
def get_ngrok_public_url():
    # ngrokのAPIにアクセスしてpublic_urlを取得する
    response = requests.get("http://localhost:4040/api/tunnels")
    tunnels = response.json()["tunnels"]
    http_tunnel = next((tunnel for tunnel in tunnels if tunnel.get("proto") == "https"), None)

    if http_tunnel is None:
        logger.error("There is no http tunnel in running ngrok instance")
        return

    public_url = http_tunnel.get("public_url")

    # public_urlを標準出力に出力する
    logger.info(f'Public URL is: {public_url}')

    return public_url


def set_webhook_url_from_ngrok():
    public_url = get_ngrok_public_url()
    set_webhook_url(public_url)


if __name__ == '__main__':
    set_webhook_url_from_ngrok()