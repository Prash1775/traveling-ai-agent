import os
import folium
from geopy.geocoders import Nominatim

def generate_map(destination):
    """Generates an interactive HTML map for the destination."""
    try:
        # Increased timeout and specific user agent for reliability
        geolocator = Nominatim(user_agent="travel_ai_agent_planner_v2")
        location = geolocator.geocode(destination, timeout=10)

        if not location:
            print(f"Location not found for: {destination}")
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

        # Use absolute path in the project root
        base_dir = os.path.dirname(os.path.abspath(__file__))
        map_file = os.path.join(os.path.dirname(base_dir), "travel_map.html")
        
        travel_map.save(map_file)
        return map_file
    except Exception as e:
        print(f"Map generation error: {e}")
        return None