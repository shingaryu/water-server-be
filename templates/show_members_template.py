
def member_contents(name: str, image_url: str) ->dict:
    contents: dict = {
        "type": "box",
        "layout": "horizontal",
        "contents": [
        {
            "type": "image",
            "url": image_url,
            "size": "xxs",
            "position": "relative",
            "aspectMode": "cover",
            "align": "start",
            "offsetStart": "sm",
            "offsetTop": "sm",
            "flex": 0
        },
        {
            "type": "text",
            "text": name,
            "flex": 0,
            "wrap": True,
            "offsetStart": "md",
            "position": "relative",
            "gravity": "center",
            "align": "start"
        }
        ],
        "position": "relative",
        "width": "100%",
        "flex": 0
    }
    return contents

def member_list_bubble(header_title: str, member_contents: list) -> dict:
    bubble: dict = {}
    bubble = {
        "type": "bubble",
        "size": "mega",
        "header": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": header_title,
              "color": "#FAFDFF",
              "weight": "bold",
              "size": "lg",
              "offsetTop": "10px",
              "offsetStart": "10px",
              "position": "absolute"
            }
          ],
          "backgroundColor": "#007AFF",
          "height": "40px",
          "justifyContent": "center"
        },
        "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "image",
              "url": "https://drive.google.com/uc?id=1zHQzyNzeKS9i1dRXJeOlC9-0bxGY3VsJ",
              "aspectMode": "cover",
              "offsetTop": "0px",
              "offsetStart": "0px",
              "aspectRatio": "1:2",
              "size": "100%"
            },
            {
              "type": "box",
              "layout": "vertical",
              "contents": member_contents,
              "position": "absolute",
              "width": "100%",
              "height": "100%",
              "offsetBottom": "none",
              "offsetTop": "none"
            }
          ],
          "paddingAll": "none",
          "flex": 0,
          "position": "relative",
          "height": "100%"
        }
    }
    return bubble
