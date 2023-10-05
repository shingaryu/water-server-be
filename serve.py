# This script is intended to be used by waitress-serve command on production server,
# including initialization of LINE bot like creating rich menu.

from dotenv import load_dotenv
load_dotenv()

import os
from common.get_logger import get_logger
from set_webhook_url import set_webhook_url
from create_rich_menu import create_rich_menu
from create_googleapi_token import create_googleapi_token

# this Flask instance is run by waitress-serve
# noinspection PyUnresolvedReferences
from main import app

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

logger.info('Initialize LINE bot...')
set_webhook_url()
create_rich_menu()
create_googleapi_token()