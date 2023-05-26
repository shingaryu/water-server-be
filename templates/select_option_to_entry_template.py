from common.consts import ENTRY_WITH_OPTION, ENTRY_WITH_OPTION_EVENT, ENTRY_WITH_OPTION_OPTION
from common.utils import format_date


def select_option_to_entry_flex_contents(event, entry_option_status):
  total_count = 0
  for (option, attendees) in entry_option_status:
    total_count += len(attendees)

  body_contents = [
    {
      "type": "text",
      "text": "投票する",
      "weight": "bold",
      "size": "xl"
    },
    {
      "type": "box",
      "layout": "vertical",
      "margin": "lg",
      "spacing": "sm",
      "contents": event_detail_lines(event, total_count)
    }
  ]

  for (option, attendees) in entry_option_status:
    body_contents.append(option_box(option["text"], attendees))
    body_contents.append(option_button(str(event["_id"]), str(option["id"])))

  contents = {
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": body_contents
    }
  }

  return contents

def event_detail_lines(event, count):
  event_detail = [
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
          "text": event["place"],
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
          "text": "日時",
          "color": "#aaaaaa",
          "size": "sm",
          "flex": 1
        },
        {
          "type": "text",
          "text": format_date(event["startTime"]),
          "wrap": True,
          "color": "#666666",
          "size": "sm",
          "flex": 5
        }
      ]
    },
    {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": f'{count}人が参加中',
          "size": "sm",
          "align": "end"
        }
      ]
    }
  ]

  return event_detail

def option_box(text, attendees):
  box = {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": text
          },
          {
            "type": "text",
            "text": str(len(attendees)),
            "align": "end"
          }
        ]
      },
      attendees_box(attendees)
    ],
    "margin": "10px"
  }

  return box

def attendees_box(attendees):
  contents = []
  for attendee in attendees:
    contents.append(
      {
        "type": "image",
        "url": attendee["pictureUrl"],
        "size": "16px"
      }
    )

    contents.append(
      {
        "type": "text",
        "text": attendee["displayName"],
        "size": "xs"
      },
    )

  box = {
    "type": "box",
    "layout": "horizontal",
    "contents": contents
  }

  return box

def option_button(event_id, option_id):
  button = {
    "type": "button",
    "action": {
      "type": "postback",
      "label": "投票",
      "data": f'{ENTRY_WITH_OPTION}/?{ENTRY_WITH_OPTION_EVENT}={event_id}&{ENTRY_WITH_OPTION_OPTION}={option_id}'
    }
  }

  return button