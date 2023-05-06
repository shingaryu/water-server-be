import os
import sys
from linebot import LineBotApi
from common.get_logger import get_logger

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

def get_line_bot_client():
    channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
    channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
    if channel_secret is None:
        logger.error('Specify LINE_CHANNEL_SECRET as environment variable.')
        sys.exit(1)
    if channel_access_token is None:
        logger.error('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
        sys.exit(1)

    line_bot_api = LineBotApi(channel_access_token)
    return line_bot_api