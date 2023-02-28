import os
import random
from datetime import date, datetime

import requests
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage


def get_weather(province: str, city: str):
    params = {"city": city, "province": province,
              "weather_type": "observe", "source": "pc"}
    res = requests.get("http://wis.qq.com/weather/common", params=params, timeout=7).json()
    return res["data"]["observe"]


def get_love_days(start_date: str):
    today = datetime.now()
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_birthday(birthday):
    today = datetime.now()
    next_birthday = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next_birthday < datetime.now():
        next_birthday = next_birthday.replace(year=next_birthday.year + 1)
    return (next_birthday - today).days + 1


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


def main():
    start_date = os.environ.get('START_DATE', '2017-06-25')
    city = os.environ.get('CITY', '武汉')
    province = os.environ.get('PROVINCE', '湖北')
    birthday = os.environ.get('BIRTHDAY', '02-11')

    app_id = os.environ["APP_ID"]
    app_secret = os.environ["APP_SECRET"]
    user_id = os.environ["USER_ID"]
    template_id = os.environ["TEMPLATE_ID"]

    client = WeChatClient(app_id, app_secret)
    print(f"start_date: {start_date}")
    print(f"city: {city}")
    print(f"birthday: {birthday}")

    wm = WeChatMessage(client)
    weather = get_weather(province, city)
    data = {
        "weather": {"value": weather.get("weather")},
        "temperature": {"value": weather.get("degree")},
        # "highest": {
        #     "value": math.floor(weather.get('high')),
        #     "color": get_random_color()
        # },
        # "lowest": {
        #     "value": math.floor(weather.get('low')),
        #     "color": get_random_color()
        # },
        "love_days": {"value": get_love_days(start_date)},
        "birthday_left": {"value": get_birthday(birthday)},
        "words": {"value": get_words(), "color": get_random_color()},
        "date": {"value": str(datetime.now().date()), "color": get_random_color()}
    }
    for i in user_id.split(","):
        res = wm.send_template(i, template_id, data)
        print(res)


if __name__ == '__main__':
    # print(get_weather("湖北", "武汉"))
    main()
