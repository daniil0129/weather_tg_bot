import requests
import datetime
from config import open_weather_token, tg_bot_token
from aiogram import Bot, Dispatcher, types, executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю тебе сводку погоды!")


@dp.message_handler()
async def get_weather(message: types.Message):
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
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

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

        await message.reply(f'****{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}****\n'
                            f'Погода в городе: {city}\nТепература: {cur_weather} C° {wd}\n'
                            f'Влажность: {humidity}%\nДаввление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n'
                            f'Восход солнца: {sunrise_timestemp}\nЗакат солнца: {sunset_timestemp}\nПродолжительность дня: {length_of_the_day}\n'
                            f'****Хорошего дня!****')
    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)
