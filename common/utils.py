from services.ngrok_service import get_ngrok_public_url


def format_date(date):
    mon = int(date.strftime("%m"))
    day = int(date.strftime("%d"))
    a = date.strftime("%a")
    hour = int(date.strftime("%H"))
    minutes = date.strftime("%M")
    text = f'{mon}/{day} ({a}) {hour}:{minutes}'
    return text


def no_icon_image_public_url():
    return f'{get_ngrok_public_url()}/static/no_icon_image.png'