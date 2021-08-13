import requests
import datetime
from config import weather_API, telegram_bot_API
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=telegram_bot_API)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def   start_command(message: types.Message):
    await message.reply("Hello! Give me a location and I will send you a weather report.")


@dp.message_handler()
async def get_weather(message: types.Message):
    description_code = {
        "Clear": "Clear \U00002600",
        "Clouds": "Clouds \U00002601",
        "Rain": "Rain \U00002614",
        "Drizzel": "Drizzel \U0001F327",
        "Thunderstorm": "Thunderstorm \U0001F329",
        "Snow": "Snow \U0001F328",
        "Mist": "Mist \U0001F32B"
    }    

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_API}&units=metric"
        )
        data = r.json()

        location = data["name"]

        weather_description = data["weather"][0]["main"]
        if weather_description in description_code:
            wd = description_code[weather_description]
        else:
            wd = "Look out the window, I don't understand the weather there!"

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        humidity = data["main"]["humidity"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        daylight_length = sunset_timestamp - sunrise_timestamp

        await message.reply(f"\n ****{datetime.datetime.now().strftime('%H:%M %d/%m/%Y')}**** \n\n"
              f"Current weather at: {location} \n{wd} \nTemperature: {temp}˚C \n"
              f"Humidity: {humidity}% \nPressure: {pressure}hPa \nWind: {wind}m/s \n"
              f"Sunrise time: {sunrise_timestamp} \nSunset time: {sunset_timestamp} \n"
              f"Length of daylight: {daylight_length} \n\n"
              f"****The End!****")

    except:
        await message.reply("\U00002620 Check the location \U00002620")


if __name__ == "__main__":
    executor.start_polling(dp)