import requests
import datetime
from pprint import pprint
from config import weather_API

print("Hello World")

def get_weather(location, weather_API):
    
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
            f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_API}&units=metric"
        )
        data = r.json()
        pprint(data)

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

        print(f"\n ****{datetime.datetime.now().strftime('%H:%M %d/%m/%Y')}**** \n"
              f"Current weather at: {location} \n{wd} \nTemperation: {temp}˚C \n"
              f"Humidity: {humidity}% \nPressure: {pressure}hPa \nWind: {wind}m/s \n"
              f"Sunrise time: {sunrise_timestamp} \nSunset time: {sunset_timestamp} \n"
              f"Length of daylight: {daylight_length} \n"
              f"The End!")

        
    except Exception as ex:
        print(ex)
        print("Check the location")

def main():
    location = input("Enter the location: ")
    get_weather(location, weather_API)

if __name__ == '__main__':
    main()