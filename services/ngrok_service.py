# ngrokは開発サーバー(main関数)とプロダクション環境では異なる起動方法を想定しています。
# 開発サーバーではpyngrokライブラリを用いてPythonプログラム内でngrokを起動します。
# プロダクション環境ではPythonプログラムとは別プロセスで、既にngrokが起動していることを前提とします。

from dotenv import load_dotenv
load_dotenv()

import os
import requests
from common.get_logger import get_logger
from pyngrok import ngrok

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

public_url = None  # キャッシュ。プログラムの起動中に変わることは想定していないので注意


def connect_http_tunnel():
    global public_url
    http_tunnel = ngrok.connect("5000", "http")
    public_url = http_tunnel.public_url
    logger.info(f'ngrok tunnel connection established on: {public_url}')
    return public_url

# キャッシュされたpublic_urlを返す。ない場合は、既に立ち上がっているngrokインスタンスのpublic_urlを取得する。
def get_ngrok_public_url():
    global public_url
    if public_url is not None:
        return public_url

    # ngrokのAPIにアクセスしてpublic_urlを取得する
    response = requests.get("http://localhost:4040/api/tunnels")
    tunnels = response.json()["tunnels"]
    http_tunnel = next((tunnel for tunnel in tunnels if tunnel.get("proto") == "https"), None)

    if http_tunnel is None:
        logger.error("There is no http tunnel in running ngrok instance")
        return

    public_url = http_tunnel.get("public_url")

    # public_urlを標準出力に出力する
    logger.info(f'ngrok http tunnel is running on: {public_url}')

    return public_url
