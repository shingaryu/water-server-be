import re
import os
import tempfile
from datetime import datetime
from pdf2image import convert_from_path
from PIL import Image
import cv2
import pytesseract

# （必要なら）Tesseract の実行パスを指定
# Windows やカスタムインストールパスの場合は以下をコメント解除して修正してください
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def pdf_to_images(pdf_path, dpi=300):
    """
    PDF ファイルを画像のリストに変換する。
    返り値: PIL.Image のリスト
    """
    return convert_from_path(pdf_path, dpi=dpi)


def preprocess_image_for_ocr(pil_img):
    """
    PIL.Image を受け取り、OpenCV で前処理した後に返す。
    - グレースケール化
    - 二値化（大津の二値化）
    - ノイズ除去（モルフォロジー変換）
    """
    # PIL -> OpenCV (NumPy) へ変換
    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    # return img

    # 1. グレースケール化
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

    #
    # # 2. 大津の二値化
    # _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #
    # # 3. モルフォロジー（膨張・収縮）でノイズを少し落ち着かせる
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

    # return processed


def ocr_image(cv2_img, lang="jpn+eng"):
    """
    OpenCV 画像（NumPy 配列）を受け取り、pytesseract で文字列を抽出して返す。
    lang 引数で使用言語（例: "jpn+eng"）を指定可能。
    """
    # OpenCV -> PIL へ変換
    pil_img = Image.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))
    text = pytesseract.image_to_string(pil_img, lang=lang)
    return text


def extract_fields(text):
    """
    OCR で得られた文字列から「金額」「日付」「名前」「用途」を
    シンプルな正規表現で抜き出す。マッチしなければ None を返す。
    """
    lines = text.splitlines()

    # １. 金額 (円マーク or “円”で終わる数字、または 1,234 形式)
    price_pattern = re.compile(r"￥?\s*([\d,]+)円?")
    price = None
    for line in lines:
        m = price_pattern.search(line.replace(" ", ""))
        if m:
            price = m.group(1).replace(",", "")
            break

    # ２. 日付 (例: 2023/06/15, 23-06-15, 令和〇年〇月〇日 など)
    # ここでは西暦 YYYY/MM/DD または YYYY-MM-DD を優先的に探す
    date_pattern1 = re.compile(r"(\d{4}[\/\-]\d{1,2}[\/\-]\d{1,2})")
    # 「令和〇年〇月〇日」などは別途処理してもよいがここでは簡易
    date_pattern2 = re.compile(r"令和\s*([0-9]+)年\s*([0-9]+)月\s*([0-9]+)日")
    date = None
    for line in lines:
        m1 = date_pattern1.search(line)
        if m1:
            date = m1.group(1)
            break
        m2 = date_pattern2.search(line)
        if m2:
            # 例: 令和5年6月1日 → 2023/06/01（西暦に変換）
            era_year = int(m2.group(1))
            era_month = int(m2.group(2))
            era_day = int(m2.group(3))
            # 令和元年は 2019年なので...
            year = 2018 + era_year
            date = f"{year}/{era_month:02d}/{era_day:02d}"
            break

    # ３. 名前 (「様」や「殿」がついている行を探す。なければ行頭に英字＋姓＋名など)
    name = None
    # 例: 「坂東　龍 様」「松澤晃樹 殿」など
    name_pattern = re.compile(r"^([\p{L}\p{Han}]+(?:\s?[\p{L}\p{Han}]+)?)\s*(?:様|殿)")
    # Unicode 正規表現を使いたいため、re.UNICODE を追加
    for line in lines:
        m = name_pattern.search(line)
        if m:
            name = m.group(1).strip()
            break

    # ４. 用途 (「体育館」「シャトル」「買い物」「領収」などキーワードベースで判定)
    usage = None
    usage_keywords = {
        "体育館": "体育館使用料",
        "シャトル": "シャトル購入",
        "マット": "マット購入",
        "本": "書籍購入",
        "飲料": "飲料購入",
        "領収": "一般支出",
    }
    for line in lines:
        for kw, label in usage_keywords.items():
            if kw in line:
                usage = label
                break
        if usage:
            break
    if not usage:
        usage = "その他"

    return {
        "金額": price,
        "日付": date,
        "名前": name,
        "用途": usage
    }


def process_receipt(path):
    """
    画像ファイル (.png/.jpg/.jpeg) または PDF (.pdf) を受け取り、
    OCR→前処理→フィールド抽出を行う。結果を辞書で返す。
    """
    # 1) PDF なら画像に変換
    imgs = []
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        pil_list = pdf_to_images(path)
        imgs = pil_list  # PIL.Image のリスト
    else:
        pil_list = [Image.open(path)]
        imgs = pil_list

    # 2) すべてのページ／画像で OCR 処理し、テキストをつなげる
    full_text = ""
    for pil_img in imgs:
        cv_img = preprocess_image_for_ocr(pil_img)
        # OpenCV 形式の画像から OCR
        page_text = ocr_image(cv_img)
        full_text += page_text + "\n"

    # 3) フィールド抽出
    fields = extract_fields(full_text)
    return fields


if __name__ == "__main__":
    import sys
    import numpy as np

    if len(sys.argv) < 2:
        print("Usage: python receipt_ocr.py <ファイルパス>")
        sys.exit(1)

    target_path = sys.argv[1]
    if not os.path.isfile(target_path):
        print(f"ファイルが見つかりません: {target_path}")
        sys.exit(1)

    result = process_receipt(target_path)
    print("===== OCR 抽出結果 =====")
    for key, value in result.items():
        print(f"{key}: {value}")
