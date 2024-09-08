# ngrokで発行したpublic URLをLINE messaging APIのwebhook URLに設定します。


from dotenv import load_dotenv
load_dotenv()

import os
from common.get_logger import get_logger
from common.line_bot_client import get_line_bot_client

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))


def set_webhook_url(public_url):
    line_bot_api = get_line_bot_client()
    line_bot_api.set_webhook_endpoint(f'{public_url}/callback')
    logger.info(f'Set webhook URL to {public_url}/callback... done!')
