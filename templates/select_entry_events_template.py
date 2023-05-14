from common.utils import format_date

def select_event_message_contents(event_flex_contents):
    contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "開催予定",
                    "weight": "bold",
                    "size": "xl"
                }] + (event_flex_contents)
        }
    }

    return contents

def event_flex_contents(datetime, place, n_attendees, postback_data):
   contents = [
        {
            "type": "separator"
        },
        {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": "日時",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": format_date(datetime),
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": "場所",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": place,
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                        }
                    ]
                },
                # {
                #     "type": "box",
                #     "layout": "baseline",
                #     "contents": [
                #         {
                #             "type": "text",
                #             "text": "人数",
                #             "flex": 1,
                #             "size": "sm",
                #             "color": "#aaaaaa"
                #         },
                #         {
                #             "type": "text",
                #             "text": f'{n_attendees}人',
                #             "flex": 5,
                #             "size": "sm"
                #         }
                #     ],
                #     "spacing": "sm"
                # }
            ]
        },
        {
            "type": "button",
            "action": {
                "type": "postback",
                "label": "参加投票",
                "data": postback_data
            }
        }
    ]

   return contents
