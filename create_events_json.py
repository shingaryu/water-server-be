import json
import calendar
import datetime
import pprint

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)

specified_month = str(int(now.strftime("%m")) + 1).zfill(2)
specified_year = now.strftime("%Y")


def extract_date_of_nth_day_of_week(year, month, nth_of_day_of_week, day_of_week):
    """
    :param year:
    :param month:
    :param nth_of_day_of_week:
    :param day_of_week: Monday(0) - Sunday(6)
    :return:
    """
    if nth_of_day_of_week < 1 or day_of_week < 0 or day_of_week > 6:
        return None

    first_day_of_week, n = calendar.monthrange(int(year), int(month))
    day = 7 * (nth_of_day_of_week - 1) + (day_of_week - first_day_of_week) % 7 + 1

    return day if day <= n else None


def extract_badminton_date(month=specified_month, year=specified_year):
    def extract_badminton_date_by_day_of_week(specified_day_of_week):
        nth_of_day_of_week = 1
        badminton_date_list_of_day_of_week = []
        while True:
            date_of_nth_day_of_week \
                = extract_date_of_nth_day_of_week(year, month, nth_of_day_of_week,
                                                  specified_day_of_week)
            if date_of_nth_day_of_week is None:
                break
            badminton_date_list_of_day_of_week.append(date_of_nth_day_of_week)
            nth_of_day_of_week += 1
        return badminton_date_list_of_day_of_week

    badminton_date_list_of_friday \
        = [year + "-" + month + "-" + str(date_of_friday).zfill(2)
           for date_of_friday in extract_badminton_date_by_day_of_week(4)]

    badminton_date_list_of_sunday \
        = [year + "-" + month + "-" + str(date_of_sunday).zfill(2)
           for date_of_sunday in extract_badminton_date_by_day_of_week(6)]

    badminton_date_list_of_specified_month \
        = [badminton_date_list_of_friday, badminton_date_list_of_sunday]

    return badminton_date_list_of_specified_month


def generate_badminton_schedule(badminton_date, day_of_week):
    shimura_2nd = [{"startTime": {"$date": badminton_date + "T18:00:00.000Z"},
                    "endTime": {"$date": badminton_date + "T21:00:00.000Z"},
                    "place": "志村第二小学校",
                    "entryOptions": [{"id": "1", "text": "18時から参加"},
                                     {"id": "2", "text": "19時過ぎから参加"},
                                     {"id": "3", "text": "不参加"}]}]

    shimura_4th = [{"startTime": {"$date": badminton_date + "T09:00:00.000Z"},
                    "endTime": {"$date": badminton_date + "T12:00:00.000Z"},
                    "place": "志村第四小学校",
                    "entryOptions": [{"id": "1", "text": "9時から参加"},
                                     {"id": "2", "text": "途中から参加"},
                                     {"id": "3", "text": "不参加"}]}]

    shingashi = [{"startTime": {"$date": badminton_date + "T09:00:00.000Z"},
                  "endTime": {"$date": badminton_date + "T12:00:00.000Z"},
                  "place": "新河岸小学校",
                  "entryOptions": [{"id": "1", "text": "9時から参加"},
                                   {"id": "2", "text": "途中から参加"},
                                   {"id": "3", "text": "不参加"}]}]

    badminton_schedule_in_selected_sports_hall = None
    if day_of_week == 0:

        badminton_schedule_in_selected_sports_hall = shimura_2nd
    elif day_of_week == 1:
        badminton_schedule_in_selected_sports_hall = shimura_4th
    return badminton_schedule_in_selected_sports_hall


def create_json(badminton_schedule):
    with open("./WaterCooler_schedule_" + specified_year + "-" + specified_month + ".json", 'w') as f:
        json.dump(badminton_schedule, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    # print(calendar.month(specified_year, specified_month))
    select_month = input(specified_year + "/" + specified_month + "のスケジュールを作成しますか？[y/n]").lower()
    if select_month in ['', 'y', 'ye', 'yes']:
        print(specified_month, "月のスケジュールを作成します")
        schedules = []
        for dow in range(len(extract_badminton_date())):
            if dow == 0:
                print("金曜日の予定を確認してください")
            elif dow == 1:
                print("日曜日の予定を確認してください")

            schedule = None
            for date_of_day_of_week in extract_badminton_date()[dow]:
                date = extract_badminton_date()[dow][
                    extract_badminton_date()[dow].index(date_of_day_of_week)]
                schedule = generate_badminton_schedule(date, dow)

                pprint.pprint(schedule)
                is_confirmed = input("この予定を確定しますか？[y/n]").lower()
                if is_confirmed in ['', 'y', 'ye', 'yes']:
                    print("確定しました")
                    schedules.append(schedule)
                elif is_confirmed in ['n', 'no']:
                    print("スキップしました")

        create_json(schedules)
        print("スケジュールの作成を完了しました")

    elif select_month in ['n', 'no']:
        print("それはまだ無理")
