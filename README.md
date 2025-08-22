# water-server-be

## リポジトリ概要
- **技術スタック**: Python 3.11 / Flask / APScheduler / line-bot-sdk / MongoDB / YouTube API / pyngrok / Waitress
- **目的**: バドミントンクラブの予定調整やメンバー・動画情報を LINE Bot や Web から管理

## ディレクトリ構成と主要モジュール
|ディレクトリ/ファイル|概要|
|---|---|
|`main.py`|Flaskアプリのエントリポイント。環境変数の読込、BluePrint登録、APSchedulerによるリマインド設定、開発向けngrok起動などを実施。|
|`serve.py`|本番サーバー用エントリ。外部で起動済みのngrokを利用し、WaitressでFlaskアプリを提供。|
|`controllers/`|HTTPルートをまとめたBluePrint群。`events_controller.py`でイベント登録・削除・表示、`linebot_controller.py`でWebhook処理、`movies_controller.py`で動画画面表示など。|
|`services/`|ビジネスロジック層。`postback_service.py`でLINEのpostbackイベント処理やFlex Message生成、`remind_service.py`でイベントリマインド、`ngrok_service.py`でトンネル管理など。|
|`repositories/`|永続化層。`mongo_repository.py`でMongoDBとのデータ操作、`youtube_repository.py`でYouTube Data APIを扱う。|
|`line_message_templates/`|LINE向けFlex Messageの雛形を辞書形式で定義。|
|`templates/`|FlaskのHTMLテンプレート。イベント一覧・登録・削除画面や動画ページなど。|
|`static/`|LINEリッチメニュー画像やダミー画像などの静的ファイル。|
|`scripts/`|補助スクリプト。Google APIトークン生成 (`create_googleapi_token.py`)、イベントJSON作成 (`create_events_json.py`) など。|

## 重要なポイント
1. **環境変数 (.env)**
   - `LINE_CHANNEL_SECRET`, `LINE_CHANNEL_ACCESS_TOKEN` などLINE Bot関連
   - `CONNECTION_STRING`, `DB_NAME` などMongoDB接続
   - `LOGGER_LEVEL`, `PORT`, `IS_YOUTUBE_FEATURE_DISABLED` 等、動作を制御する設定
2. **外部サービスとの連携**
   - LINE Messaging API: Webhook経由でユーザー入力を受け、Flex MessageやQuick Replyで応答
   - YouTube Data API: 最新動画やプレイリストを取得して表示
   - ngrok: 開発時に外部からアクセス可能なURLを生成
3. **スケジューラ**
   - APSchedulerで `remind_service.remind_closest_event` を定期実行し、イベント前日にリマインドを送信
4. **MongoDBスキーマ（概略）**
   - `Events`: 開催日時・場所・参加オプションなど
   - `Entries`: ユーザーごとの参加表明
   - `MemberInfo` 相当の集計データは `mongo_repository.generate_member_info_dict` で生成

## 次に学ぶべき内容・手順の目安
1. **ローカル環境構築**
   - `poetry install` で依存関係をインストール
   - `.env` に必要な環境変数を設定
   - MongoDB・LINEチャネル・ngrokなど外部サービスを用意
2. **動作確認**
   - 開発: `python main.py` を実行し、`http://localhost:PORT` と LINE Webhook を接続
   - 本番相当: `python serve.py` でngrokの既存トンネルを利用しWaitressサーバーを起動
3. **コードリーディングのガイド**
   - ルーティング: `controllers/` のBluePrintでHTTP/LINEイベントの流れを把握
   - ビジネスロジック: `services/` の各サービスでFlex MessageやDB操作を確認
   - データアクセス: `repositories/mongo_repository.py` のCRUD処理を参照
   - UI/メッセージテンプレート: `templates/` と `line_message_templates/` で画面とLINEメッセージの定義を学習
4. **拡張・改善の例**
   - 新しいLINE postbackイベントを追加する場合、`postback_service.py` と `linebot_controller.py` を追う
   - MongoDBスキーマ変更や集計処理は `mongo_repository.py` を確認
   - フロントエンドの拡張は `templates/` と `static/` に新しいファイルを追加

## 補足リソース
- Flask公式ドキュメント
- LINE Messaging API & Flex Message仕様
- APScheduler、MongoDB、Google APIs (YouTube) それぞれの公式リファレンス

