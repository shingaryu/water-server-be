import json

from common.consts import ENTRY_WITH_OPTION, ENTRY_WITH_OPTION_EVENT, ENTRY_WITH_OPTION_OPTION
from common.utils import format_date

WATER_COOLER_BLUE = "#007AFF"
MIDNIGHT_BLUE = "#001E43"
FROSTY_BLUE = "#BBDBF3"
SMOKE_BLUE = "#A4C1D7"
SNOW_WHITE = "#FAFDFF"
TRANSPARENT = "#00000000"


def select_option_to_entry_flex_contents(event, entry_option_status):
    entry_option_status = create_test_attendees_list(entry_option_status, 3, 7, 5)  # 複数人UIテスト用

    total_count = 0
    for (option, attendees) in entry_option_status:
        total_count += len(attendees)

    gym_img_url = load_gym_img_url(event)
    attendees_list = create_attendees_list(entry_option_status)

    height_of_attendees_list_of_registered_block = "140px"
    height_of_body_block = "360px"
    tmp = len(entry_option_status[0][1])
    if len(entry_option_status[0][1]) >= 7 or len(entry_option_status[1][1]) >= 7:
        attendees_length = len(entry_option_status[0][1])
        if len(entry_option_status[0][1]) < len(entry_option_status[1][1]):
            attendees_length = len(entry_option_status[1][1])

        height_of_attendees_list_of_registered_block = str(140 + (20*(attendees_length-6))) + "px"
        height_of_body_block = str(360 + (20*(attendees_length-6))) + "px"


    tmp = len(attendees_list[0].get("contents")) / 2

    container_config = {
        "type": "bubble",
        "size": "mega",
    }
    header_block = {
        "header": {
            "type": "box",
            "layout": "vertical",
            "height": "40px",
            "contents": [
                {
                    "type": "text",
                    "text": format_date(event["startTime"]) + " 参加登録",
                    "color": SNOW_WHITE,
                    "position": "absolute",
                    "weight": "bold",
                    "size": "lg",
                    "offsetTop": "10px",
                    "offsetStart": "10px"
                }
            ],
            "background": {
                "type": "linearGradient",
                "angle": "160deg",
                "startColor": WATER_COOLER_BLUE,
                "endColor": FROSTY_BLUE,
                "centerPosition": "50%",
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
                    "url": gym_img_url
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": event["place"],
                            "color": SNOW_WHITE,
                            "weight": "regular",
                        }

                    ],
                    "position": "absolute",
                    "backgroundColor": MIDNIGHT_BLUE + "AA",
                    "cornerRadius": "xxl",
                    "alignItems": "center",
                    "width": "150px",
                    "height": "20px",
                    "offsetEnd": "-15px",
                    "offsetTop": "10px"
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
                                        "color": MIDNIGHT_BLUE,
                                        "weight": "bold",
                                        "decoration": "underline"
                                    }, {
                                        "type": "text",
                                        "text": str(len(entry_option_status[0][1])),
                                        "color": MIDNIGHT_BLUE,
                                        "weight": "regular",
                                        "align": "end"
                                    },
                                ]
                            },
                            attendees_list[0],

                        ],
                        "backgroundColor": MIDNIGHT_BLUE + "08",
                        "flex": 1,
                        "width": "48%",
                        "height": height_of_attendees_list_of_registered_block,
                        "borderWidth": "2px",
                        "cornerRadius": "xs"
                    },
                    {
                        "type": "separator",
                        "margin": "md",
                        "color": TRANSPARENT
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
                                        "color": MIDNIGHT_BLUE,
                                        "weight": "bold",
                                        "decoration": "underline"
                                    }, {
                                        "type": "text",
                                        "text": str(len(entry_option_status[1][1])),
                                        "color": MIDNIGHT_BLUE,
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
                        "backgroundColor": MIDNIGHT_BLUE + "08",
                        "flex": 1,
                        "height": height_of_attendees_list_of_registered_block,
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
                                "color": MIDNIGHT_BLUE,
                                "weight": "bold",
                                "decoration": "underline"
                            }, {
                                "type": "text",
                                "text": str(len(entry_option_status[2][1])),
                                "color": MIDNIGHT_BLUE,
                                "weight": "regular",
                                "align": "end"
                            }
                        ]
                    },
                    attendees_list[2]
                ],
                "width": "100%",
                "height": "45px",
                "backgroundColor": MIDNIGHT_BLUE + "08",
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
                        "margin": "lg",
                        "color": TRANSPARENT
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
                                        "color": SNOW_WHITE,
                                        "weight": "bold"
                                    }
                                ],
                                "borderWidth": "normal",
                                "borderColor": WATER_COOLER_BLUE,
                                "cornerRadius": "xxl",
                                "height": "40px",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "backgroundColor": WATER_COOLER_BLUE + "EE",
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
                                "color": TRANSPARENT
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "途中参加",
                                        "color": SNOW_WHITE,
                                        "weight": "bold"
                                    }
                                ],
                                "borderWidth": "normal",
                                "borderColor": WATER_COOLER_BLUE,
                                "cornerRadius": "xxl",
                                "height": "40px",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "backgroundColor": WATER_COOLER_BLUE + "EE",
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
                        "color": TRANSPARENT
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "不参加",
                                "color": SNOW_WHITE,
                                "weight": "regular"
                            }
                        ],
                        "borderWidth": "none",
                        "cornerRadius": "xxl",
                        "height": "40px",
                        "alignItems": "center",
                        "backgroundColor": SMOKE_BLUE + "AA",
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
                            "color": MIDNIGHT_BLUE,
                            "weight": "bold",
                            "size": "lg",
                            "align": "end",
                        }, {
                            "type": "text",
                            "text": f"({total_count}人登録中)",
                            "color": MIDNIGHT_BLUE,
                            "weight": "regular",
                            "size": "md",
                            "align": "start",
                        },
                    ],
                },
                {
                    "type": "separator",
                    "margin": "sm",
                    "color": TRANSPARENT
                },
                registered_block,
                {
                    "type": "separator",
                    "margin": "sm",
                    "color": TRANSPARENT
                },
                voting_block,
            ],
            "margin": "none",
            "height": height_of_body_block,
            "spacing": "none"
        }
    }

    contents = container_config
    container_config.update(header_block)
    container_config.update(hero_block)
    container_config.update(body_block)

    return contents


def load_gym_img_url(event):
    gym_img_url = ""
    if event["place"] == "志村第二小学校":
        gym_img_url = "https://drive.google.com/uc?id=19pMDPJ4TbrMiHzfV92Ul65Y-sWmiB2qy"

    elif event["place"] == "志村第四小学校":
        gym_img_url = "https://drive.google.com/uc?id=17PcFtGXbCNtZwxjaod2aKBXQxog5eNFx"

    else:
        gym_img_url = "https://drive.google.com/uc?id=1vDEYGexYhEime4QIrWc9owtK053bzt6M"

    return gym_img_url


def create_attendees_list(entry_option_status):
    attendees_list = []
    for (option, attendees) in entry_option_status:
        if "1" in option.values():
            attendees_list.append(attendees_box(attendees))

        elif "2" in option.values():
            attendees_list.append(attendees_box(attendees))

        elif "3" in option.values():
            attendees_list.append(absentees_box(attendees))

    return attendees_list


def attendees_box(attendees):
    contents = []
    for attendee in attendees:
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "image",
                    "url": attendee["pictureUrl"],
                    "size": "18px",
                    "position": "absolute",
                    "offsetStart": "4px"

                }, {
                    "type": "text",
                    "text": attendee["displayName"],
                    "size": "14px",
                    "offsetStart": "26px",
                },
            ]
        })
        contents.append({
            "type": "separator",
            "margin": "xs",
            "color": TRANSPARENT
        })

    box = {
        "type": "box",
        "layout": "vertical",
        "contents": contents
    }
    return box


def absentees_box(absentees):
    contents = [{
        "type": "box",
        "layout": "horizontal",
        "contents": [{
            "type": "text",
            "text": "→",
            "color": TRANSPARENT,
        }]
    }]

    for loop_count, absentee in enumerate(absentees):
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "position": "absolute",
            "offsetStart": str(20 * loop_count + 4) + "px",
            "contents": [
                {
                    "type": "image",
                    "url": absentee["pictureUrl"],
                    "size": "18px",

                }, {
                    "type": "text",
                    "text": absentee["displayName"],
                    "size": "14px",
                    "color": MIDNIGHT_BLUE + "00"
                },
            ]
        })

    box = {
        "type": "box",
        "layout": "horizontal",
        "contents": contents

    }
    return box


def create_test_attendees_list(entry_option_status, sanka, tochu, fusan):
    test_entry_option_status = entry_option_status
    attendee = test_entry_option_status[0][1][0]
    test_entry_option_status[0][1].clear()
    test_entry_option_status[1][1].clear()
    test_entry_option_status[2][1].clear()

    for s in range(sanka):
        test_entry_option_status[0][1].append(attendee)
    for t in range(tochu):
        test_entry_option_status[1][1].append(attendee)
    for f in range(fusan):
        test_entry_option_status[2][1].append(attendee)

    return test_entry_option_status
