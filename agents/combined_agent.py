import google.generativeai as genai
from utils.api_keys import GEMINI_API_KEY

def get_combined_travel_data(destination, days, interests):
    """Get both recommendations and itinerary using Gemini API (Cloud Ready)."""
    
    if not GEMINI_API_KEY or "AIza" not in GEMINI_API_KEY:
        return "AI Error: Valid Gemini API Key not found. Please set it in utils/api_keys.py"

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')

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

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Gemini API Error: {str(e)}"
