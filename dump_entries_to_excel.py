import os
import pandas as pd
from repositories.mongo_repository import find_all_events, find_all_entries
from common.get_logger import get_logger

logger = get_logger(__name__, os.environ.get("LOGGER_LEVEL"))

logger.info(f"すべてのEntryを集計します…")

# Entryデータの取得
entry_data = find_all_entries()

# Eventデータの取得
event_data = find_all_events()

# pandasのDataFrameにデータを変換
data = []
for entry in entry_data:
    entry_id = str(entry["_id"])
    user_id = entry["user"]["userId"]
    display_name = entry["user"]["displayName"]
    event_id = entry["eventId"]
    selected_option_id = entry["selectedOptionId"]

    # selectedOptionIdに対応するテキストをEventデータから取得
    event = next((e for e in event_data if str(e["_id"]) == event_id), None)

    if event is None:
        selected_option_text = ""
        start_time = ""
        place = ""
    else:
        selected_option_text = next(
            (option["text"] for option in event["entryOptions"] if option["id"] == selected_option_id), None)

        start_time = event["startTime"]
        place = event["place"]

    data.append(
        [entry_id, user_id, display_name, event_id, start_time, place, selected_option_id, selected_option_text])

# pandasのDataFrameを作成
df = pd.DataFrame(data,
                  columns=["entryId", "userId", "displayName", "eventId", "startTime", "place", "selectedOptionId",
                           "selectedOptionText"])

# Excelファイルに出力
output_file = "all_entries.xlsx"
df.to_excel(output_file, index=False)

logger.info(f"すべてのEntryを{output_file}に保存しました。")
