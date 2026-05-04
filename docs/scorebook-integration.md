# 記録用Webアプリ連携メモ

## (背景)記録用Webアプリとの連携
本アプリの利用者の一人が個人で公開している記録用アプリがある。(index (1).htmlとして仮で本リポジトリに取り込んだものと同様と思われる)
https://oioi1020.github.io/bado_doubles/app.html

### 実現したいこと
- Water Server (本リポジトリのLINEアプリ)から上記記録用アプリに遷移したとき、Water Cooler(本アプリの利用者達が所属する団体の名前)に関連する記録だけを表示したい

### 分かっていること
- 記録用アプリはデータをブラウザのローカルに保存する


## 結論
現時点で Water Server 側だけで実装できる範囲は、「Water Server から開いた記録用アプリを Water Cooler 専用の保存領域で起動する」こと。

このリポジトリ内の `/badminton-scorebook` は `?group=Water%20Cooler` を受け取ると、ブラウザの localStorage キーを通常版とは分ける。これにより、Water Server のリンクから入力した記録だけが Water Cooler 用として表示される。

外部公開版 `https://oioi1020.github.io/bado_doubles/app.html` の既存データを Water Cooler だけに絞り込むには、公開版側の実装変更が必要。理由は、localStorage はオリジン単位で隔離され、Water Server から GitHub Pages 側の保存データを読むことも書き換えることもできないため。


## Water Server 側の実装
- `/water-cooler-scorebook?tab=record` にアクセスすると、`/badminton-scorebook?tab=record&group=Water+Cooler` へリダイレクトする。
- LINE リッチメニューの記録アプリリンクは `group=Water+Cooler` 付きのURLを開く。
- `SCOREBOOK_GROUP_NAME` 環境変数でグループ名を変更できる。
- `SCOREBOOK_APP_URL` 環境変数を設定すると、リッチメニューの遷移先を外部公開版に差し替えられる。ただし、外部公開版が `group` クエリを解釈するまでは絞り込み効果はない。

## 先方アプリに依頼したい最小仕様
外部公開版でも次のURLをサポートしてもらう。

```text
https://oioi1020.github.io/bado_doubles/app.html?group=Water%20Cooler&tab=record
```

期待動作:
- `group` または `groupId` クエリを読む。
- localStorage の既存データ内に同名または同IDのグループがあれば、そのグループを active にする。
- 該当グループがなければ、未作成として案内するか、自動作成するかを事前に決める。
- `tab=record|stats|settings` が指定されていれば該当タブを開く。
- グループが active になった状態では、そのグループに属する試合と記録だけを表示する。

## このリポジトリ側(index (1).html改変)で作った連携案
- `/water-cooler-scorebook?tab=record` から開くと、`/badminton-scorebook?tab=record&group=Water+Cooler` に遷移する
- `templates/index (1).html` は `group` クエリを受け取り、localStorage の保存キーを Water Cooler 用に分ける
- そのため、Water Server から開いた記録用アプリでは Water Cooler 用リンク経由で保存した記録だけが表示される
- LINEリッチメニューの記録アプリリンクも `group=Water+Cooler` 付きのURLを開く
- グループ名は `SCOREBOOK_GROUP_NAME` 環境変数で変更できる


## 相談ポイント
- グループ判定は表示名 `Water Cooler` でよいか、安定した `groupId` を発行するか。
- グループ未作成時に自動作成するか、ユーザーに手動作成を促すか。
- Water Server から渡すURL仕様を `group` にするか `groupId` にするか。
- 既存ユーザーがすでに公開版に保存している記録を Water Cooler グループへ移す導線を用意するか。
- GitHub Pages の公開版と Water Server 配下のローカル版では localStorage が共有されないため、どちらを正式利用先にするか。

## 発展：複数人でのデータ共有
Q. Water ServerのユーザーAが記録アプリに移動し記録アプリ側で結果を入力 → Water Serverの別ユーザーBがその結果を見ることはできますか？ 

A. 現状(上記の構想)のままでは、基本的に **ユーザーBは見られません**。

理由は、記録アプリの結果が **ユーザーAのブラウザの `localStorage` に保存されるだけ**だからです。`group=Water Cooler` は「Aのブラウザ内で保存領域を分ける」だけで、Water Server や他人のブラウザには共有されません。

例外的に見られるケースはあります:
- AとBが同じ端末・同じブラウザ・同じブラウザプロファイルを使う
- AがJSON/CSVを書き出して、Bが手動で読み込む

自動共有したいなら、記録データをサーバーに保存する必要があります。

**必要な変更**
Water Server 側:
- MongoDBなどに記録アプリ用の共有データを保存する
- 例: `ScorebookGroups`, `ScorebookMatches`, `ScorebookRecords` のようなコレクションを追加
- APIを追加する
  - `GET /api/scorebook/groups/water-cooler`
  - `POST /api/scorebook/groups/water-cooler/records`
  - `PATCH /api/scorebook/records/{record_id}`
  - `DELETE /api/scorebook/records/{record_id}`
- ユーザー認証・権限確認を入れる
  - 最低限は共有トークン付きURL
  - ちゃんとやるなら LIFF / LINE Login でLINEユーザーを識別
- 外部公開版から呼ぶなら CORS 設定も必要

記録アプリ側:
- `localStorage` を主保存先にするのをやめる
- 起動時に Water Server API から Water Cooler の記録を取得する
- 記録追加・編集・削除時に Water Server API へ送信する
- `localStorage` は一時キャッシュやオフライン用に限定する
- `?group=Water%20Cooler` または `?groupId=water-cooler` を読んで対象グループを決める
- 複数人が同時編集する前提で、更新失敗・競合・再読み込みを扱う

一番現実的な構成は、**Water Serverを記録データの共有バックエンドにして、記録アプリはUIとして使う**形です。公開版をそのまま使う場合でも、先方アプリに「Water Server APIと同期する機能」を入れてもらう必要があります。