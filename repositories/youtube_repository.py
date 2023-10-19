from __future__ import print_function

import os.path
from dotenv import load_dotenv
load_dotenv()

from common.get_logger import get_logger
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
api_service_name = "youtube"
api_version = "v3"

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', scopes)
else:
    raise Exception("token.jsonがありません。")


def refresh_token_if_expired():
    if not creds.expired:
        return
    if not creds.refresh_token:
        return
    logger.debug("token expired. refreshing...")
    creds.refresh(Request())
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    logger.debug("token refresh completed")


refresh_token_if_expired()
youtube = build(api_service_name, api_version, credentials=creds)


def get_my_recent_videos():
    logger.info("get my recent videos...")
    refresh_token_if_expired()
    request = youtube.search().list(
        part="snippet",
        maxResults=50,  # YouTube APIの単一のリクエストで取得できる最大数
        forMine=True,
        type="video",
        order="date"
    )

    response = request.execute()
    logger.debug(response)
    return response.get("items")
