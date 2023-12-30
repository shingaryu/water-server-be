from dotenv import load_dotenv

from common.consts import SHOW_EVENTS, SHOW_NEXT_EVENT, AKIO_BUTTON, SHOW_VIDEOS, SHOW_MEMBERS

load_dotenv()

from linebot.models import (
    RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, PostbackAction
)
import os
import datetime
from common.get_logger import get_logger
from common.line_bot_client import get_line_bot_client

# 実行ディレクトリからの相対パスとして解釈されるため、本スクリプトは必ず同ディレクトリで実行すること
RICH_MENU_IMAGE_PATH = "richmenu_image.jpg"
POSTBACK_DATA = [
    f'{SHOW_NEXT_EVENT}',
    f'{SHOW_EVENTS}',
    f'{SHOW_MEMBERS}',
    f'richmenu/?area=3',
    f'{SHOW_VIDEOS}',
    f'{AKIO_BUTTON}'
]

DISPLAY_TEXTS = [
    '参加登録',
    '開催日一覧',
    'メンバーリスト',
    'bWVtYmVyIGxpc3Q=',
    'ムービー',
    'はやしあきお',
]

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

def create_rich_menu():
    line_bot_api = get_line_bot_client()

    logger.info('Delete all rich menus...')
    rich_menu_list = line_bot_api.get_rich_menu_list()
    for rich_menu in rich_menu_list:
        logger.debug(f'Deleting {rich_menu.rich_menu_id}')
        line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)

    now = datetime.datetime.now()
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=1686),
        selected=True,
        name="water-server-menu_" + now.strftime("%Y-%m-%d_%H-%M-%S"),
        chat_bar_text='メニュー',
        areas=[RichMenuArea(
            bounds=RichMenuBounds(x=(i % 3) * 833, y=(i // 3) * 843, width=833, height=843),
            action=PostbackAction(data=POSTBACK_DATA[i], display_text=DISPLAY_TEXTS[i])) for i in range(6)]
    )
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    logger.info(f'Rich menu created: {rich_menu_id}')

    with open(RICH_MENU_IMAGE_PATH, 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, "image/jpeg", f)
        logger.info(f'Rich menu image was successfully set by: {RICH_MENU_IMAGE_PATH}')

    line_bot_api.set_default_rich_menu(rich_menu_id)
    logger.info(f'Rich menu was successfully set as default menu')

if __name__ == '__main__':
    create_rich_menu()