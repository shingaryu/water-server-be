def select_option_to_entry_flex_contents():
    contents = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
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
            "contents": [
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
                    "text": "志村第五小学校",
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
                    "text": "5/22 (金) 18:00 - 21:00",
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
                    "text": "6人が参加中",
                    "size": "sm",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "18:00から参加"
                  },
                  {
                    "type": "text",
                    "text": "(投票済み)3",
                    "align": "end"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "image",
                    "url": "https://profile.line-scdn.net/0m04331b447251a512c9d51c1608b0d8c42fc9d3de96f1",
                    "size": "16px"
                  },
                  {
                    "type": "text",
                    "text": "松澤晃樹",
                    "size": "xs"
                  },
                  {
                    "type": "image",
                    "url": "https://profile.line-scdn.net/0m04331b447251a512c9d51c1608b0d8c42fc9d3de96f1",
                    "size": "16px"
                  },
                  {
                    "type": "text",
                    "text": "松澤晃樹",
                    "size": "xs"
                  },
                  {
                    "type": "image",
                    "url": "https://profile.line-scdn.net/0m04331b447251a512c9d51c1608b0d8c42fc9d3de96f1",
                    "size": "16px"
                  },
                  {
                    "type": "text",
                    "text": "松澤晃樹",
                    "size": "xs"
                  }
                ]
              }
            ],
            "margin": "5px"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "投票",
              "data": "entry_with_option=1"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "19:00から参加"
                  },
                  {
                    "type": "text",
                    "text": "3",
                    "align": "end"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "image",
                    "url": "https://profile.line-scdn.net/0m04331b447251a512c9d51c1608b0d8c42fc9d3de96f1",
                    "size": "16px"
                  },
                  {
                    "type": "text",
                    "text": "松澤晃樹",
                    "size": "xs"
                  },
                  {
                    "type": "image",
                    "url": "https://profile.line-scdn.net/0m04331b447251a512c9d51c1608b0d8c42fc9d3de96f1",
                    "size": "16px"
                  },
                  {
                    "type": "text",
                    "text": "松澤晃樹",
                    "size": "xs"
                  },
                  {
                    "type": "image",
                    "url": "https://profile.line-scdn.net/0m04331b447251a512c9d51c1608b0d8c42fc9d3de96f1",
                    "size": "16px"
                  },
                  {
                    "type": "text",
                    "text": "松澤晃樹",
                    "size": "xs"
                  }
                ]
              }
            ],
            "margin": "5px"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "投票",
              "data": "entry/?event=6456313426165d3c40069c2f&option=2"
            }
          }
        ]
      }
    }


    return contents