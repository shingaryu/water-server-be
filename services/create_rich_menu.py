import datetime
import os

from dotenv import load_dotenv
from linebot.constants import PostbackInputOption
from linebot.models import (
    PostbackAction,
    RichMenu,
    RichMenuArea,
    RichMenuBounds,
    RichMenuSize,
    URIAction,
)

from common.consts import SHOW_EVENTS, SHOW_MEMBERS, SHOW_NEXT_EVENT, SHOW_VIDEOS
from common.get_logger import get_logger
from common.line_bot_client import get_line_bot_client
from common.scorebook_links import scorebook_target_url
from services.ngrok_service import current_ngrok_public_url

load_dotenv()

RICH_MENU_IMAGE_PATH = "./static/richmenu_image.jpg"
RICH_MENU_WIDTH = 2500
RICH_MENU_HEIGHT = 1686
CELL_WIDTH = 833
CELL_HEIGHT = 843
BOTTOM_RIGHT_X = CELL_WIDTH * 2
BOTTOM_RIGHT_Y = CELL_HEIGHT
AKIO_WIDTH_LEFT = 416
AKIO_WIDTH_RIGHT = RICH_MENU_WIDTH - BOTTOM_RIGHT_X - AKIO_WIDTH_LEFT
AKIO_HEIGHT_TOP = 421
AKIO_HEIGHT_BOTTOM = RICH_MENU_HEIGHT - BOTTOM_RIGHT_Y - AKIO_HEIGHT_TOP

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))


def create_rich_menu():
    base_url = current_ngrok_public_url()
    line_bot_api = get_line_bot_client()

    actions = [
        PostbackAction(
            data=SHOW_NEXT_EVENT,
            display_text="show next event",
            input_option=PostbackInputOption.CLOSE_RICH_MENU,
        ),
        PostbackAction(
            data=SHOW_EVENTS,
            display_text="show events",
            input_option=PostbackInputOption.CLOSE_RICH_MENU,
        ),
        PostbackAction(
            data=SHOW_MEMBERS,
            display_text="show members",
            input_option=PostbackInputOption.CLOSE_RICH_MENU,
        ),
        PostbackAction(
            data="richmenu/?area=3",
            display_text="richmenu area 3",
            input_option=PostbackInputOption.CLOSE_RICH_MENU,
        ),
        PostbackAction(
            data=SHOW_VIDEOS,
            display_text="show videos",
            input_option=PostbackInputOption.CLOSE_RICH_MENU,
        ),
    ]

    logger.info("Delete all rich menus...")
    for rich_menu in line_bot_api.get_rich_menu_list():
        logger.debug(f"Deleting {rich_menu.rich_menu_id}")
        line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)

    now = datetime.datetime.now()
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=RICH_MENU_WIDTH, height=RICH_MENU_HEIGHT),
        selected=True,
        name="water-server-menu_" + now.strftime("%Y-%m-%d_%H-%M-%S"),
        chat_bar_text="menu",
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=(i % 3) * CELL_WIDTH,
                    y=(i // 3) * CELL_HEIGHT,
                    width=CELL_WIDTH,
                    height=CELL_HEIGHT,
                ),
                action=actions[i],
            )
            for i in range(5)
        ]
        + [
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=BOTTOM_RIGHT_X,
                    y=BOTTOM_RIGHT_Y,
                    width=AKIO_WIDTH_LEFT,
                    height=AKIO_HEIGHT_TOP,
                ),
                action=URIAction(
                    uri=scorebook_target_url(base_url, tab="record"),
                    label="scorebook record",
                ),
            ),
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=BOTTOM_RIGHT_X + AKIO_WIDTH_LEFT,
                    y=BOTTOM_RIGHT_Y,
                    width=AKIO_WIDTH_RIGHT,
                    height=AKIO_HEIGHT_TOP,
                ),
                action=URIAction(
                    uri=scorebook_target_url(base_url, tab="stats"),
                    label="scorebook stats",
                ),
            ),
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=BOTTOM_RIGHT_X,
                    y=BOTTOM_RIGHT_Y + AKIO_HEIGHT_TOP,
                    width=AKIO_WIDTH_LEFT,
                    height=AKIO_HEIGHT_BOTTOM,
                ),
                action=URIAction(
                    uri=scorebook_target_url(base_url, tab="settings"),
                    label="scorebook settings",
                ),
            ),
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=BOTTOM_RIGHT_X + AKIO_WIDTH_LEFT,
                    y=BOTTOM_RIGHT_Y + AKIO_HEIGHT_TOP,
                    width=AKIO_WIDTH_RIGHT,
                    height=AKIO_HEIGHT_BOTTOM,
                ),
                action=URIAction(
                    uri=f"{base_url}/events/register",
                    label="event register",
                ),
            ),
        ],
    )

    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    logger.info(f"Rich menu created: {rich_menu_id}")

    with open(RICH_MENU_IMAGE_PATH, "rb") as image_file:
        line_bot_api.set_rich_menu_image(rich_menu_id, "image/jpeg", image_file)
        logger.info(f"Rich menu image was successfully set by: {RICH_MENU_IMAGE_PATH}")

    line_bot_api.set_default_rich_menu(rich_menu_id)
    logger.info("Rich menu was successfully set as default menu")


if __name__ == "__main__":
    create_rich_menu()
