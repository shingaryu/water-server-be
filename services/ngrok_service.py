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

def current_ngrok_public_url():
    global public_url
    return public_url

def store_ngrok_public_url(url):
    global public_url
    public_url = url

def connect_http_tunnel(port):
    global public_url
    http_tunnel = ngrok.connect(port, "http")
    public_url = http_tunnel.public_url
    logger.info(f'ngrok tunnel connection established on: {public_url}')
    return public_url

def initiallize_with_external_ngrok(port):
    public_url = fetch_ngrok_public_url(port)
    store_ngrok_public_url(public_url)
    return public_url

# 既に立ち上がっているngrokインスタンスのpublic_urlを取得する。
# この場合、pythonのngrokモジュールを使用すると同時起動のためエラーになる。そのためlocalhostでホストされているngrokの管理用APIを使用する
def fetch_ngrok_public_url(port):
    # ngrokのAPIにアクセスしてpublic_urlを取得する
    response = requests.get("http://localhost:4040/api/tunnels")
    tunnels = response.json()["tunnels"]
    http_tunnel = next((tunnel for tunnel in tunnels if tunnel.get("proto") == "https" and f":{port}" in tunnel.get("config").get("addr")), None)

    if http_tunnel is None:
        logger.error(f"There is no http tunnel on port {port} in running ngrok instance")
        return

    public_url = http_tunnel.get("public_url")

    # public_urlを標準出力に出力する
    logger.info(f'ngrok http tunnel on port {port} is running on: {public_url}')

    return public_url
