from config import open_weather_token
import requests
import datetime
from pprint import pprint


def get_weather(city, open_weather_token):

    code_to_smile = {
        'Clear': "Ясно \U00002600",
        'Clouds': "Облачно \U00002601",
        'Rain': "Дождь \U00002614",
        'Drizzle': "Дождь \U00002614",
        'Thunderstorm': "Гроза \U000026A1",
        'Snow': "Снег \U0001F328",
        'Mist': "Туман \U0001F32B",

    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        # pprint(data) #moscow

        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно!"

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestemp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestemp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = sunset_timestemp - sunrise_timestemp

        print(f'****{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}****\n'
              f'Погода в городе: {city}\nТепература: {cur_weather} C° {wd}\n'
              f'Влажность: {humidity}%\nДаввление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n'
              f'Восход солнца: {sunrise_timestemp}\nЗакат солнца: {sunset_timestemp}\nПродолжительность дня: {length_of_the_day}\n'
              f'Хорошего дня!')

    except Exception as ex:
        print(ex)
        print("Проверьте название города")


def main():
    city = input('Введите горолд: ')
    get_weather(city, open_weather_token)


if __name__ == '__main__':
    main()