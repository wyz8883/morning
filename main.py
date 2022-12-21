import math
import os
import random
from datetime import date, datetime

import requests
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage


def get_weather(city: str):
    url = f"http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&" \
          f"clientType=android&sign=android&city={city}"
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp'])


def get_love_days(start_date: str):
    today = datetime.now()
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_birthday(birthday):
    today = datetime.now()
    next_birthday = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next_birthday < datetime.now():
        next_birthday = next_birthday.replace(year=next_birthday.year + 1)
    return (next_birthday - today).days


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
    birthday = os.environ.get('BIRTHDAY', '02-11')

    app_id = os.environ["APP_ID"]
    app_secret = os.environ["APP_SECRET"]
    user_id = os.environ["USER_ID"]
    template_id = os.environ["TEMPLATE_ID"]

    client = WeChatClient(app_id, app_secret)

    wm = WeChatMessage(client)
    wea, temperature = get_weather(city)
    data = {
        "weather": {"value": wea}, "temperature": {"value": temperature},
        "love_days": {"value": get_love_days(start_date)},
        "birthday_left": {"value": get_birthday(birthday)},
        "words": {"value": get_words(), "color": get_random_color()},
        "date": {"value": str(datetime.now().date())}
    }
    for i in user_id.split(","):
        res = wm.send_template(i, template_id, data)
        print(res)


if __name__ == '__main__':
    main()
