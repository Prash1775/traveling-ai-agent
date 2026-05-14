import ollama

def get_combined_travel_data(destination, days, interests):
    """Get both recommendations and itinerary in a single AI call to save time."""
    
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

    try:
        response = ollama.chat(
            model='llama3',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']
    except Exception as e:
        return f"AI Generation Error (Check if Ollama is running): {str(e)}"
