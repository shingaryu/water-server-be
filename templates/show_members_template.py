
def member_contents_demo(name: str, image_url: str) ->dict:
    contents: dict = {
        "type": "bubble",
        "size": "micro",
        "hero": {
            "type": "image",
            "url": image_url,
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "320:213"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": name,
                    "weight": "bold",
                    "size": "sm",
                    "wrap": True
                }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        }
    }

    return contents

def member_contents(name: str, image_url: str) ->dict:
    contents = {}
    return contents
