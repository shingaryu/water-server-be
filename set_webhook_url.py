# ngrokを立ち上げた状態でこのスクリプトを実行してください。
# ngrokは、環境変数PATHに設定されている場合、以下のコマンドで実行できます。
# ngrok http 5000

from dotenv import load_dotenv
load_dotenv()

import os
import requests
import subprocess
from common.get_logger import get_logger
from common.line_bot_client import get_line_bot_client

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

PUBLIC_URL_ENV_KEY = 'PUBLIC_URL'

def store_variable_to_env_file(key, value):
    logger.debug(f'subprocessでdotenvコマンドを実行します…')
    command = f'dotenv set {key} {value}'

    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f'dotenvコマンドの実行に失敗しました。{e}')
        raise
    except Exception as e:
        logger.error(f'subprocessでのコマンド実行において予期しないエラーが発生しました。{e}')
        raise

def set_webhook_url():
    line_bot_api = get_line_bot_client()

    # ngrokのAPIにアクセスしてpublic_urlを取得する
    response = requests.get("http://localhost:4040/api/tunnels")
    public_url = response.json()["tunnels"][0]["public_url"]

    # public_urlを標準出力に出力する
    logger.info(f'Public URL is: {public_url}')

    line_bot_api.set_webhook_endpoint(f'{public_url}/callback')
    logger.info(f'Set webhook URL to {public_url}/callback... done!')

    try:
        store_variable_to_env_file(PUBLIC_URL_ENV_KEY, public_url)
        logger.info(f'Public URLを.envファイルに保存しました。{PUBLIC_URL_ENV_KEY}={public_url}')
    except Exception as e:
        logger.error(f'.envファイルの保存でエラーが発生しました。')
        raise


if __name__ == '__main__':
    set_webhook_url()