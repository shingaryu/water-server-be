from dotenv import load_dotenv
load_dotenv()

import os
import subprocess
import requests
import time
from common.get_logger import get_logger
from common.line_bot_client import get_line_bot_client

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))
line_bot_api = get_line_bot_client()

# ngrokはPATHに設定しておくこと
# ngrokを実行するコマンド
#cmd = "start ngrok http 5000" # todo: linux 対応

#logger.info(f'Execute {cmd}...')
#ngrok_process = subprocess.Popen(cmd.split(), shell=True)

# ngrokが起動するまで待機する
#time.sleep(2)

# ngrokのAPIにアクセスしてpublic_urlを取得する
response = requests.get("http://localhost:4040/api/tunnels")
public_url = response.json()["tunnels"][0]["public_url"]

# public_urlを標準出力に出力する
logger.info(f'Public URL is: {public_url}')

line_bot_api.set_webhook_endpoint(f'{public_url}/callback')
logger.info(f'Set webhook URL to {public_url}/callback... done!')