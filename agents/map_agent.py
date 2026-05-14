import os
import folium
from geopy.geocoders import Nominatim

def generate_map(destination):
    """Generates an interactive folium Map object for the destination."""
    try:
        geolocator = Nominatim(user_agent="travel_ai_agent_planner_v2")
        location = geolocator.geocode(destination, timeout=10)

        if not location:
            return None

        latitude = location.latitude
        longitude = location.longitude

        travel_map = folium.Map(
            location=[latitude, longitude],
            zoom_start=12
        )

        folium.Marker(
            [latitude, longitude],
            popup=destination,
            tooltip="Destination"
        ).add_to(travel_map)

        return travel_map
    except Exception as e:
        print(f"Map generation error: {e}")
        return None