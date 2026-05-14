def get_activities(destination, days, interests):

    itinerary = ""

    for day in range(1, days + 1):

        itinerary += f"""
Day {day}

🌅 Morning:
Explore famous places in {destination}

🍴 Afternoon:
Try local food and cafes

🌇 Evening:
Shopping and sightseeing

🎯 Interests:
{interests}

--------------------------------
"""

    return itinerary