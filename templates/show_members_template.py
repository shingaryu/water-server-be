LOGO_BACKGROUND_COLOR = "#F3F2F9"

def member_contents(name: str, image_url: str, total_attendance: str) ->dict:
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
            "flex": 0,
            "action": {
                "type": "uri",
                "uri": image_url
            }
        },
        {
            "type": "text",
            "text": name,
            "wrap": True,
            "offsetStart": "md",
            "position": "relative",
            "gravity": "center",
            "align": "start",
            "weight": "bold"
        },
        {
          "type": "text",
          "text": total_attendance,
          "flex": 0,
          "weight": "bold",
          "gravity": "center",
          "wrap": True,
          "offsetEnd": "xs"
        }
        ],
        "position": "relative",
        "width": "100%",
        "flex": 0
    }
    return contents


def member_list_bubble(header_title: str, member_contents: list) -> dict:
    bubble: dict = {
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
              "size": "full",
              "flex": 0,
              "position": "absolute"
            },
            {
              "type": "box",
              "layout": "vertical",
              "contents": member_contents,
              "position": "relative",
              "width": "100%",
              "height": "100%",
              "offsetBottom": "none",
              "offsetTop": "none"
            }
          ],
          "paddingAll": "sm",
          "flex": 0,
          "position": "relative",
          "height": "100%",
          "backgroundColor": LOGO_BACKGROUND_COLOR
        }
    }
    return bubble
