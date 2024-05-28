from dotenv import load_dotenv

from common.consts import SHOW_EVENTS, SHOW_NEXT_EVENT, SHOW_VIDEOS, SHOW_MEMBERS, AKIO_BUTTON
from services.ngrok_service import current_ngrok_public_url

load_dotenv()

from linebot.models import (
    RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, PostbackAction, URIAction
)
import os
import datetime
from common.get_logger import get_logger
from common.line_bot_client import get_line_bot_client

# 実行ディレクトリからの相対パスとして解釈されるため、本スクリプトは必ず同ディレクトリで実行すること
RICH_MENU_IMAGE_PATH = "richmenu_image.jpg"

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

def create_rich_menu():
    actions = [
        PostbackAction(data=f'{SHOW_NEXT_EVENT}', display_text='参加登録'),
        PostbackAction(data=f'{SHOW_EVENTS}', display_text='開催日一覧'),
        PostbackAction(data=f'{SHOW_MEMBERS}', display_text='メンバーリスト'),
        PostbackAction(data=f'richmenu/?area=3', display_text='bWVtYmVyIGxpc3Q='),
        PostbackAction(data=f'{SHOW_VIDEOS}', display_text='ムービー'),
        URIAction(uri=f'{current_ngrok_public_url()}/events/register', label='開催日の登録')
    ]

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
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(x=(i % 3) * 833, y=(i // 3) * 843, width=833, height=843),
                action=actions[i]) for i in range(5)
        ] + [
            RichMenuArea(
                bounds=RichMenuBounds(x=5 % 3 * 833, y=5 // 3 * 843, width=833, height=843 * 3 / 4), # 右下を除く3/4の領域
                action=PostbackAction(data=f'{AKIO_BUTTON}', display_text='はやしあきお')
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=5 % 3 * 833 + 833 * 3 / 4, y=5 // 3 * 843 + 843 * 3 / 4, width=833 / 4, height=843 / 4), # 右下1/4の領域(隠し機能とするため)
                action=URIAction(uri=f'{current_ngrok_public_url()}/events/register', label='開催日の登録')
            )
        ]
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