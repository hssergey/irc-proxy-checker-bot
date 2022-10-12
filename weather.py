import traceback
import requests
from settings import openweathermap_key

KELVIN = 273.15

def get_weather(city):
    try:
        response = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={openweathermap_key}&lang=ru')
        data = response.json()
        code = int(data["cod"])
        if not code == 200:
            return data["message"]
        response_city = data["city"]["name"]
        weather_strings = []
        skip = 0
        max_strings = 3
        for weather_block in data["list"]:
            if skip % 3 == 0:
                weather_strings.append(parse_weather_block(weather_block))
            skip += 1
            if len(weather_strings) >= max_strings:
                break
        weather = "\n".join(weather_strings)
        result = f'Погода в г.{response_city} {weather}'
        return result
    except Exception as ex:
        traceback.print_exc()
        return str(ex)


def parse_weather_block(block):
    date = block["dt_txt"]
    temperature = int(block["main"]["temp"] - KELVIN)
    description = block["weather"][0]["description"]
    return f'на {date}: {description}, {temperature} градусов'


if __name__ == '__main__':
    import sys
    args = sys.argv
    print(get_weather(args[1]))        