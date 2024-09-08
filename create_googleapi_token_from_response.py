import json
from datetime import datetime, timedelta

with open('scripts/credentials_web_flow.json', 'r') as file:
    credentials = json.load(file)

with open('playground_response.json', 'r') as file:
    response = json.load(file)

# 新しいトークン情報を作成
new_token_info = {
    "token": response["access_token"],
    "refresh_token": response["refresh_token"],
    "token_uri": credentials["web"]["token_uri"],
    "client_id": credentials["web"]["client_id"],
    "client_secret": credentials["web"]["client_secret"],
    "scopes": [response["scope"]],
    # "expiry": (datetime.utcnow() + timedelta(seconds=data["expires_in"])).isoformat() + 'Z',
    "expiry": "1970-01-01T00:00:00Z" # 変換後に強制的にリフレッシュをさせるため、固定
}

# 新しいトークン情報をtoken.jsonに書き込む
with open('token.json', 'w') as file:
    json.dump(new_token_info, file, indent=4)

print("token.json has been updated.")
