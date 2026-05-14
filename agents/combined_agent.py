from groq import Groq
import os

try:
    from utils.api_keys import GROQ_API_KEY
except ImportError:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_combined_travel_data(destination, days, interests):
    """Get both recommendations and itinerary using Groq API (High Performance)."""
    
    if not GROQ_API_KEY or "gsk" not in GROQ_API_KEY:
        return "AI Error: Valid Groq API Key not found. Please set it in utils/api_keys.py"

    try:
        client = Groq(api_key=GROQ_API_KEY)

        prompt = f"""
        You are an expert travel guide. Create a complete travel plan for {destination} for {days} days.
        The traveler's interests are: {interests}

        Please provide a response with the following structured sections:
        
        1. 🎯 RECOMMENDATIONS
           - 🏛️ Top Tourist Places
           - 🍽️ Best Restaurants & Local Food
           - ☕ Popular Cafes
           - 🎯 Must-try Activities & Experiences

        2. 📅 DAY-BY-DAY ITINERARY
           For each of the {days} days, provide:
           - 🌅 Morning: Activity
           - ☀️ Afternoon: Activity & Lunch spot
           - 🌙 Evening: Activity & Dinner spot

        Keep the tone professional and helpful.
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Groq API Error: {str(e)}"
