"""
共通関数
"""


def format_date(date):
    mon = int(date.strftime("%m"))
    day = int(date.strftime("%d"))
    a = date.strftime("%a")
    hour = int(date.strftime("%H"))
    minutes = date.strftime("%M")
    text = f'{mon}/{day} ({a}) {hour}:{minutes}'
    return text