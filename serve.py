# This script is intended to be executed on the production server,
# including initialization of LINE bot like creating rich menu.

from dotenv import load_dotenv

from services.ngrok_service import initiallize_with_external_ngrok

load_dotenv()

import os
from common.get_logger import get_logger
from services.set_webhook_url import set_webhook_url
from services.create_rich_menu import create_rich_menu
from main import app, port_to_serve
from waitress import serve

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

logger.info('Initialize LINE bot...')
public_url = initiallize_with_external_ngrok(port_to_serve)
set_webhook_url(public_url)
create_rich_menu()
serve(app, listen=f'*:{port_to_serve}')  # both IPv4 and IPv6
