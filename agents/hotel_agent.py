import requests
import os

try:
    from utils.api_keys import RAPID_API_KEY
except ImportError:
    RAPID_API_KEY = os.getenv("RAPID_API_KEY")

# FAST MOCK FALLBACK
MOCK_HOTELS = [

    {
        "name": "Grand Palace Hotel",
        "stars": 5,
        "price_per_night": 5000,
        "booking_link": "https://www.booking.com"
    },

    {
        "name": "City Comfort Inn",
        "stars": 3,
        "price_per_night": 2500,
        "booking_link": "https://www.booking.com"
    },

    {
        "name": "Budget Stay Lodge",
        "stars": 2,
        "price_per_night": 1200,
        "booking_link": "https://www.booking.com"
    }
]

def search_hotels(city):

    # NO API KEY
    if (
        not RAPID_API_KEY
        or
        RAPID_API_KEY == "YOUR_RAPIDAPI_KEY_HERE"
    ):

        return MOCK_HOTELS

    try:

        url = (
            "https://booking-com.p.rapidapi.com/"
            "v1/hotels/locations"
        )

        querystring = {
            "name": city,
            "locale": "en-gb"
        }

        headers = {
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host":
            "booking-com.p.rapidapi.com"
        }

        response = requests.get(
            url,
            headers=headers,
            params=querystring,
            timeout=5
        )

        data = response.json()

        # API FAILED
        if (
            not isinstance(data, list)
            or
            len(data) == 0
        ):

            return MOCK_HOTELS

        hotels = []

        for item in data[:3]:

            hotels.append({

                "name":
                item.get(
                    "name",
                    "Unknown Hotel"
                ),

                "stars":
                item.get(
                    "hotel_class",
                    3
                ),

                "price_per_night":
                3000,

                "booking_link":
                "https://www.booking.com"

            })

        return hotels

    except Exception as e:

        print(
            f"Hotel API Error: {e}"
        )

        return MOCK_HOTELS