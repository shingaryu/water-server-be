from common.consts import ENTRY_WITH_OPTION, ENTRY_WITH_OPTION_EVENT, ENTRY_WITH_OPTION_OPTION
from common.utils import format_date, no_icon_image_public_url

WATER_COOLER_BLUE = "#007AFF"
MIDNIGHT_BLUE = "#001E43"
FROSTY_BLUE = "#BBDBF3"
SMOKE_BLUE = "#A4C1D7"
SNOW_WHITE = "#FAFDFF"
TRANSPARENT = "#00000000"

ATTENDEES_LIST_INDEX_ATTENDEES = 0
ATTENDEES_LIST_INDEX_HALFWAYS = 1
ATTENDEES_LIST_INDEX_ABSENTEES = 2

ENTRY_OPTION_ID_ATTEND = "1"
ENTRY_OPTION_ID_HALFWAY = "2"
ENTRY_OPTION_ID_ABSENT = "3"


def select_option_to_entry_flex_contents(event, entry_option_status):
    # entry_option_status = create_test_attendees_list(entry_option_status, 10, 0, 12)  # 複数人UIテスト用

    total_count = 0
    for (option, attendees) in entry_option_status:
        total_count += len(attendees)

    gym_img_url = load_gym_img_url(event)

    # 注: entry_option_status内の要素は順序を保証しない(例: "id":2 のoptionが先頭に来る場合もある)が、create_attendees_listの返り値は順序を保証している
    attendees_list, n_registered_list = create_attendees_list(entry_option_status)

    min_height_of_attendees_list = "140px"

    n_attendees = n_registered_list[ATTENDEES_LIST_INDEX_ATTENDEES]
    n_halfways = n_registered_list[ATTENDEES_LIST_INDEX_HALFWAYS]
    n_absentees = n_registered_list[ATTENDEES_LIST_INDEX_ABSENTEES]

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
            "backgroundColor": WATER_COOLER_BLUE,
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
                                        "text": str(n_attendees),
                                        "color": MIDNIGHT_BLUE,
                                        "weight": "regular",
                                        "align": "end"
                                    },
                                ]
                            },
                            attendees_list[ATTENDEES_LIST_INDEX_ATTENDEES],

                        ],
                        "backgroundColor": MIDNIGHT_BLUE + "08",
                        "flex": 1,
                        "width": "48%",
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
                        "contents": [],
                        "height": min_height_of_attendees_list
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
                                        "text": str(n_halfways),
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
                                    attendees_list[ATTENDEES_LIST_INDEX_HALFWAYS],
                                ]
                            }
                        ],
                        "backgroundColor": MIDNIGHT_BLUE + "08",
                        "flex": 1,
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
                                "text": str(n_absentees),
                                "color": MIDNIGHT_BLUE,
                                "weight": "regular",
                                "align": "end"
                            }
                        ]
                    },
                    attendees_list[ATTENDEES_LIST_INDEX_ABSENTEES]
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
                    "size": "300px", # 相対値[%]で指定した場合、デバイスによって挙動が大きく変わる(原因不明)
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
            "spacing": "none"
        }
    }

    contents = container_config
    container_config.update(header_block)
    container_config.update(hero_block)
    container_config.update(body_block)

    return contents


def load_gym_img_url(event):
    if event["place"] == "志村第二小学校":
        gym_img_url = "https://drive.google.com/uc?id=19pMDPJ4TbrMiHzfV92Ul65Y-sWmiB2qy"

    elif event["place"] == "志村第四小学校":
        gym_img_url = "https://drive.google.com/uc?id=1BuemrYDy0Gq_vbAUP_Xi1Ly82FSHUynR"

    else:
        gym_img_url = "https://drive.google.com/uc?id=11JTurANpTrHuWhDTXlInnntWOZvouQK-"

    return gym_img_url


def create_attendees_list(entry_option_status):
    attendees_list = [None] * 3
    entry_option_dict = {}
    for (option, attendees) in entry_option_status:
        entry_option_dict[option["id"]] = attendees

    # todo: id:1 -> 参加, id:2 -> 途中参加, id:3 -> 不参加 の定義付け
    attendees_list[ATTENDEES_LIST_INDEX_ATTENDEES] = attendees_box(entry_option_dict.get(ENTRY_OPTION_ID_ATTEND, []))
    attendees_list[ATTENDEES_LIST_INDEX_HALFWAYS] = attendees_box(entry_option_dict.get(ENTRY_OPTION_ID_HALFWAY, []))
    attendees_list[ATTENDEES_LIST_INDEX_ABSENTEES] = absentees_box(entry_option_dict.get(ENTRY_OPTION_ID_ABSENT, []))

    n_registered_list = [None] * 3
    n_registered_list[ATTENDEES_LIST_INDEX_ATTENDEES] = len(entry_option_dict.get(ENTRY_OPTION_ID_ATTEND, []))
    n_registered_list[ATTENDEES_LIST_INDEX_HALFWAYS] = len(entry_option_dict.get(ENTRY_OPTION_ID_HALFWAY, []))
    n_registered_list[ATTENDEES_LIST_INDEX_ABSENTEES] = len(entry_option_dict.get(ENTRY_OPTION_ID_ABSENT, []))

    return attendees_list, n_registered_list


def attendees_box(attendees):
    contents = []
    for attendee in attendees:
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "4px",
            "paddingStart": "4px",
            "paddingEnd": "4px",
            "contents": [
                {
                    "type": "image",
                    "flex": 0,
                    "url": attendee["pictureUrl"] or no_icon_image_public_url(),
                    "size": "18px",
                }, {
                    "type": "text",
                    "flex": 0,
                    "text": attendee["displayName"],
                    "size": "14px",
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


# だいたい12人目以降が見切れる
def absentees_box(absentees):
    contents = []
    for loop_count, absentee in enumerate(absentees):
        contents.append({
                    "type": "image",
            "flex": 0,
                    "url": absentee["pictureUrl"] or no_icon_image_public_url(),
                    "size": "18px",
            "margin": "4px"
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
