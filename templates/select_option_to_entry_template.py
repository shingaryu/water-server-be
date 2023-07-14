from common.consts import ENTRY_WITH_OPTION, ENTRY_WITH_OPTION_EVENT, ENTRY_WITH_OPTION_OPTION
from common.utils import format_date


def attendees_box(attendees):
    contents = []
    for attendee in attendees:
        contents.append(
            {
                "type": "image",
                "url": attendee["pictureUrl"],
                "size": "18px",
                "position": "absolute",
                "offsetStart": "4px"

            },
        )

        contents.append(
            {
                "type": "text",
                "text": attendee["displayName"],
                "size": "14px",
                "offsetStart": "26px",
            },
        )

    box = {
        "type": "box",
        "layout": "horizontal",
        "contents": contents
    }
    return box


def absentees_box(absentees):
    contents = []
    for absentee in absentees:
        contents.append(
            {
                "type": "image",
                "url": absentee["pictureUrl"],
                "size": "18px",
                "position": "absolute",
                "offsetStart": "4px"

            }
        )

        contents.append(
            {
                "type": "text",
                "text": absentee["displayName"],
                "size": "14px",
                "offsetStart": "26px",
                "color": "#00000000"
            },
        )

    box = {
        "type": "box",
        "layout": "horizontal",
        "contents": contents
    }
    return box


def select_option_to_entry_flex_contents(event, entry_option_status):
    total_count = 0
    for (option, attendees) in entry_option_status:
        total_count += len(attendees)

    attendees_list = []
    for (option, attendees) in entry_option_status:
        tmp = option["id"]
        if "1" in option.values():
            attendees_list.append(attendees_box(attendees))

        elif "2" in option.values():
            attendees_list.append(attendees_box(attendees))

        elif "3" in option.values():
            attendees_list.append(absentees_box(attendees))

    container_config = {
        "type": "bubble",
        "size": "mega",
        "direction": "ltr",
    }
    header_block = {
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": format_date(event["startTime"]) + " 参加登録",
                    "color": "#F2F2F7",
                    "weight": "bold",
                    "size": "lg"
                }
            ],
            "background": {
                "type": "linearGradient",
                "angle": "160deg",
                "startColor": "#007AFF",
                "endColor": "#64D2FF",
                "centerPosition": "50%"
            }
        }
    }
    hero_block = {
        "hero": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "size": "full",
                    "aspectRatio": "32:9",
                    "aspectMode": "cover",
                    "position": "absolute",
                    "offsetTop": "0px",
                    "offsetStart": "0px",
                    "url": "https://drive.google.com/uc?id=1BuemrYDy0Gq_vbAUP_Xi1Ly82FSHUynR"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": event["place"],
                            "color": "#F2F2F7AA",
                            "weight": "regular",
                        }

                    ],
                    "position": "absolute",
                    "backgroundColor": "#001E43AA",
                    "cornerRadius": "xxl",
                    "alignItems": "center",
                    "width": "150px",
                    "height": "40px",
                    "offsetEnd": "-15px",
                    "offsetBottom": "-20px"
                },
            ],
            "height": "80px"
        }
    }
    registered_block = {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "参加　",
                                        "color": "#001E43",
                                        "weight": "bold",
                                        "decoration": "underline"
                                    }, {
                                        "type": "text",
                                        "text": str(len(entry_option_status[0][1])),
                                        "color": "#001E43",
                                        "weight": "regular",
                                        "align": "end"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    attendees_list[0],
                                ]
                            }
                        ],
                        # "borderColor": "#007AFF",
                        "backgroundColor": "#001E4308",
                        "flex": 1,
                        "width": "48%",
                        "height": "140px",
                        "borderWidth": "2px",
                        "cornerRadius": "xs"
                    },
                    {
                        "type": "separator",
                        "margin": "md",
                        "color": "#00000000"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "途中参加　",
                                        "color": "#001E43",
                                        "weight": "bold",
                                        "decoration": "underline"
                                    }, {
                                        "type": "text",
                                        "text": str(len(entry_option_status[1][1])),
                                        "color": "#001E43",
                                        "weight": "regular",
                                        "align": "end"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    attendees_list[1],
                                ]
                            }
                        ],
                        # "borderColor": "#007AFF",
                        "backgroundColor": "#001E4308",
                        "flex": 1,
                        "height": "140px",
                        "width": "48%",
                        "borderWidth": "2px",
                        "cornerRadius": "xs"
                    }
                ],
                "justifyContent": "center"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "不参加　",
                                "color": "#001E43",
                                "weight": "bold",
                                "decoration": "underline"
                            }, {
                                "type": "text",
                                "text": str(len(entry_option_status[2][1])),
                                "color": "#001E43",
                                "weight": "regular",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    attendees_list[2],
                                ]
                            }
                        ]
                    }
                ],
                "width": "100%",
                "height": "60px",
                # "borderColor": "#007AFF",
                "backgroundColor": "#001E4308",
                "borderWidth": "2px",
                "margin": "sm",
                "spacing": "none",
                "cornerRadius": "xs"
            }
        ]
    }
    voting_block = {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "separator",
                        "margin": "md",
                        "color": "#00000000"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "参加",
                                        "color": "#F2F2F7",
                                        "weight": "bold"
                                    }
                                ],
                                "borderWidth": "normal",
                                "borderColor": "#007AFF",
                                "cornerRadius": "xxl",
                                "height": "40px",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "backgroundColor": "#007AFFEE",
                                "action": {
                                    "type": "postback",
                                    "label": "action",
                                    "data": f'{ENTRY_WITH_OPTION}/?{ENTRY_WITH_OPTION_EVENT}=' + str(event["_id"]) +
                                            f'&{ENTRY_WITH_OPTION_OPTION}=1'
                                }
                            },
                            {
                                "type": "separator",
                                "margin": "xs",
                                "color": "#00000000"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "途中参加",
                                        "color": "#F2F2F7",
                                        "weight": "bold"
                                    }
                                ],
                                "borderWidth": "normal",
                                "borderColor": "#007AFF",
                                "cornerRadius": "xxl",
                                "height": "40px",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "backgroundColor": "#007AFFEE",
                                "action": {
                                    "type": "postback",
                                    "label": "action",
                                    "data": f'{ENTRY_WITH_OPTION}/?{ENTRY_WITH_OPTION_EVENT}=' + str(event["_id"]) +
                                            f'&{ENTRY_WITH_OPTION_OPTION}=2'
                                }

                            }
                        ]
                    },
                    {
                        "type": "separator",
                        "margin": "sm",
                        "color": "#00000000"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "不参加",
                                "color": "#F2F2F7",
                                "weight": "regular"
                            }
                        ],
                        "borderWidth": "none",
                        "cornerRadius": "xxl",
                        "height": "40px",
                        "alignItems": "center",
                        "backgroundColor": "#001E4344",
                        "justifyContent": "center",
                        "action": {
                            "type": "postback",
                            "label": "action",
                            "data": f'{ENTRY_WITH_OPTION}/?{ENTRY_WITH_OPTION_EVENT}=' + str(event["_id"]) +
                                    f'&{ENTRY_WITH_OPTION_OPTION}=3'
                        }
                    }
                ]
            }
        ]
    }
    body_block = {
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": "https://drive.google.com/uc?id=1zHQzyNzeKS9i1dRXJeOlC9-0bxGY3VsJ",
                    "position": "absolute",
                    "offsetTop": "0px",
                    "offsetStart": "0px",
                    "aspectRatio": "1:2",
                    "size": "120%",
                    "aspectMode": "cover"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "登録状況",
                            "color": "#001E43",
                            "weight": "bold",
                            "size": "lg",
                            "align": "end"
                        }, {
                            "type": "text",
                            "text": f"({total_count}人登録中)",
                            "color": "#001E43",
                            "weight": "regular",
                            "size": "md",
                            "align": "start"
                        },
                    ],

                },
                {
                    "type": "separator",
                    "margin": "sm",
                    "color": "#00000000"
                },
                registered_block,
                {
                    "type": "separator",
                    "margin": "sm",
                    "color": "#00000000"
                },
                voting_block,
            ],
            "margin": "none",
            "height": "360px",
            "spacing": "none"
        }
    }

    contents = container_config
    container_config.update(header_block)
    container_config.update(hero_block)
    container_config.update(body_block)

    return contents
