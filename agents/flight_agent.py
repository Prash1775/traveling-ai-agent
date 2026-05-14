import requests
import random

from utils.api_keys import AVIATIONSTACK_API_KEY

# FAST FALLBACK FLIGHTS
MOCK_FLIGHTS = [

    {
        "airline": "IndiGo",
        "price": 4500,
        "time": "09:00 AM",
        "booking_link": "https://www.skyscanner.com"
    },

    {
        "airline": "Air India",
        "price": 5200,
        "time": "12:30 PM",
        "booking_link": "https://www.skyscanner.com"
    },

    {
        "airline": "SpiceJet",
        "price": 3900,
        "time": "06:45 PM",
        "booking_link": "https://www.skyscanner.com"
    }
]

def search_flights(source, destination):

    # NO API KEY
    if (
        not AVIATIONSTACK_API_KEY
        or
        AVIATIONSTACK_API_KEY == "https://booking-com15.p.rapidapi.com/api/v1/cars/searchCarRentals"
    ):

        return MOCK_FLIGHTS

    try:

        url = (
            "http://api.aviationstack.com/v1/flights"
        )

        params = {
            "access_key":
            AVIATIONSTACK_API_KEY
        }

        response = requests.get(
            url,
            params=params,
            timeout=5
        )

        data = response.json()

        # BAD API RESPONSE
        if (
            "data" not in data
            or
            len(data["data"]) == 0
        ):

            return MOCK_FLIGHTS

        flights = []

        for item in data["data"][:3]:

            airline = item.get(
                "airline",
                {}
            ).get(
                "name",
                "Unknown Airline"
            )

            departure = item.get(
                "departure",
                {}
            ).get(
                "scheduled",
                "N/A"
            )

            flights.append({

                "airline": airline,

                "price":
                random.randint(3000, 9000),

                "time": departure,

                "booking_link":
                "https://www.skyscanner.com"

            })

        return flights

    except Exception as e:

        print(
            f"Flight API Error: {e}"
        )

        return MOCK_FLIGHTS