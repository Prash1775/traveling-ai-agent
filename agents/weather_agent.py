import requests
import os

try:
    from utils.api_keys import WEATHER_API_KEY
except ImportError:
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city):

    # NO API KEY
    if (
        not WEATHER_API_KEY
        or
        WEATHER_API_KEY == "a53cf7b4744a2bb92735f9944e5de1ba"
    ):

        return "Clear sky, 28°C"

    try:

        url = (
            "https://api.openweathermap.org/"
            "data/2.5/weather"
        )

        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }

        response = requests.get(
            url,
            params=params,
            timeout=5
        )

        data = response.json()

        # BAD RESPONSE
        if "weather" not in data:

            return "Weather unavailable"

        weather = data["weather"][0][
            "description"
        ]

        temp = data["main"]["temp"]

        return f"{weather}, {temp}°C"

    except Exception as e:

        print(
            f"Weather API Error: {e}"
        )

        return "Weather unavailable"