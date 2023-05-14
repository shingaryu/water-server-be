mock_events = [
    {
        "_id": {
            "$oid": "6456313426165d3c40069c2f"
        },
        "startTime": "2023-05-22T18:00:00+09:00",
        "endTime": "2023-05-22T21:00:00+09:00",
        "place": "志村第五小学校",
        "entryOptions": [
            {
                "id": "1",
                "text": "18:00から参加"
            },
            {
                "id": "2",
                "text": "19:00から参加"
            },
            {
                "id": "3",
                "text": "不参加"
            }
        ]
    },
    {
        "_id": {
            "$oid": "6456318526165d3c40069c30"
        },
        "startTime": "2023-05-14T09:00:00+09:00",
        "endTime": "2023-05-14T12:00:00+09:00",
        "place": "桜台体育館",
        "entryOptions": [
            {
                "id": "1",
                "text": "9:00から参加"
            },
            {
                "id": "2",
                "text": "途中から"
            },
            {
                "id": "3",
                "text": "☓"
            }
        ]
    }
]

mock_entries = [
    {
      "_id": {
        "$oid": "6460fe41f743fbf3cfa47cba"
      },
      "eventId": "6456313426165d3c40069c2f",
      "user": {
        "userId": "Ufd40f0203a59aea10cd60c3a07bb391d",
        "displayName": "松澤晃樹",
        "pictureUrl": "https://profile.line-scdn.net/0m04331b447251a512c9d51c1608b0d8c42fc9d3de96f1",
        "statusMessage": "ポケモンが とてもきもちよさそうに ねています",
        "language": "ja"
      },
      "selectedOptionId": "1"
    },
    {
      "_id": {
        "$oid": "646100dcf743fbf3cfa47cbb"
      },
      "eventId": "6456313426165d3c40069c2f",
      "user": {
        "userId": "Ufd40f0203a59aea10cd60c3a07bb391d",
        "displayName": "あきお2",
        "pictureUrl": "https://profile.line-scdn.net/0m04331b447251a512c9d51c1608b0d8c42fc9d3de96f1",
        "statusMessage": "ポケモンが とてもきもちよさそうに ねています",
        "language": "ja"
      },
      "selectedOptionId": "3"
    }
]
