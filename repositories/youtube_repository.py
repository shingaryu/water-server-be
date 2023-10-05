from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', scopes)
else:
    raise Exception("token.jsonがありません。")

if creds.expired and creds.refresh_token:
    creds.refresh(Request())
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

api_service_name = "youtube"
api_version = "v3"

youtube = build(api_service_name, api_version, credentials=creds)

my_channel_id = None

def get_my_channel():
    try:
        request = youtube.channels().list(
            part="snippet",
            mine=True
        )

        response = request.execute()

        return response.get("items")[0]
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

def init_my_channel_id():
    global my_channel_id
    if my_channel_id is None:
        my_channel_id = get_my_channel().get("id")

def get_my_recent_videos():
    init_my_channel_id()

    request = youtube.search().list(
        part="snippet",
        maxResults=50,  # YouTube APIの単一のリクエストで取得できる最大数
        channelId=my_channel_id,
        type="video",
        order="date"
    )

    response = request.execute()
    # print(response)
    return response.get("items")
