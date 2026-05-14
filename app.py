import gradio as gr
import asyncio

from agents.chatbot_agent import ask_ai
from agents.weather_agent import get_weather
from agents.hotel_agent import search_hotels
from agents.flight_agent import search_flights
from agents.budget_agent import calculate_budget
from agents.combined_agent import get_combined_travel_data
from agents.pdf_agent import generate_pdf 
from agents.map_agent import generate_map 
from agents.memory_agent import save_memory, load_memory

# ============================================
# MAIN TRAVEL PLANNER FUNCTION
# ============================================

async def travel_planner(
    username,
    source,
    destination,
    days,
    budget,
    interests
):
    save_memory(
        username,
        {
            "destination": destination,
            "interests": interests,
            "budget": budget
        }
    ) 
    memory = load_memory(username)

    if not source or not destination:
        return "⚠️ Please enter both Source and Destination."

    # START PARALLEL AGENT REQUESTS
    tasks = [
        asyncio.to_thread(get_weather, destination),                     # Sync -> Thread
        asyncio.to_thread(search_hotels, destination),                   # Sync -> Thread
        asyncio.to_thread(search_flights, source, destination),          # Sync -> Thread
        asyncio.to_thread(get_combined_travel_data, destination, int(days), interests) # Combined AI Call
    ]

    # Gather all results
    results = await asyncio.gather(*tasks, return_exceptions=True)

    weather = results[0] if not isinstance(results[0], Exception) else "Weather unavailable"
    hotels = results[1] if not isinstance(results[1], Exception) else []
    flights = results[2] if not isinstance(results[2], Exception) else []
    ai_content = results[3] if not isinstance(results[3], Exception) else "No travel details available"

    # ============================================
    # HOTEL DETAILS
    # ============================================

    hotel_name = "Hotel Not Found"
    hotel_cost = 0

    try:
        if hotels and len(hotels) > 0:
            hotel = hotels[0]
            hotel_name = hotel.get("name", "Hotel Not Found")
            hotel_cost = hotel.get("price_per_night", 5000)
    except Exception:
        pass

    # ============================================
    # FLIGHT DETAILS
    # ============================================

    flight_airline = "N/A"
    flight_price = 0
    flight_time = "N/A"

    try:
        if flights and len(flights) > 0:
            flight = flights[0]
            flight_airline = flight.get("airline", "N/A")
            flight_price = flight.get("price", 0)
            flight_time = flight.get("time", "N/A")
    except Exception:
        pass

    # ============================================
    # BUDGET
    # ============================================

    budget_report = calculate_budget(
        budget,
        hotel_cost * int(days),
        flight_price
    )

    # ============================================
    # FINAL RESULT
    # ============================================

    result = f"""
====================================
🌍 TRAVELING AI AGENT
====================================

📍 Destination : {destination}

🛫 Source      : {source}

📅 Duration    : {int(days)} Days

====================================
🌦️ WEATHER
====================================

{weather}

====================================
✈️ FLIGHT DETAILS
====================================

Airline : {flight_airline}

Price   : ₹{flight_price:,}

Time    : {flight_time}

====================================
🏨 HOTEL DETAILS
====================================

Hotel            : {hotel_name}

Cost Per Night   : ₹{hotel_cost:,}

Total Hotel Cost : ₹{hotel_cost * int(days):,}

====================================
💰 BUDGET REPORT
====================================

Total Budget  : ₹{budget:,}

Total Expense : ₹{budget_report["expense"]:,}

Remaining     : ₹{budget_report["remaining"]:,}

{ai_content}

====================================
🤖 POWERED BY OLLAMA AI
====================================
"""

    return result


# ============================================
# CHATBOT FUNCTION
# ============================================

async def chatbot(message, history):

    response = await asyncio.to_thread(ask_ai, message)

    if history is None:
        history = []

    history.append({
        "role": "user",
        "content": message
    })

    history.append({
        "role": "assistant",
        "content": response
    })

    return "", history

async def generate_trip_pdf(
    username,
    source,
    destination,
    days,
    budget,
    interests
):
    result = await travel_planner(
        username,
        source,
        destination,
        days,
        budget,
        interests
    )

    pdf_file = await asyncio.to_thread(generate_pdf, result)
    return pdf_file


# ============================================
# GRADIO UI
# ============================================

css_code = """
.container { max-width: 900px; margin: auto; padding-top: 20px; }
.gr-button { border-radius: 8px; transition: all 0.3s ease; }
.gr-button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.gr-form { border-radius: 12px; background: rgba(255,255,255,0.05); padding: 20px; }
"""

async def generate_map_async(destination):
    return await asyncio.to_thread(generate_map, destination)

with gr.Blocks(
    title="Traveling AI Agent"
) as app:

    gr.Markdown("""
# 🌍 Traveling AI Agent

### AI Powered Smart Travel Planner

Plan smarter trips using:
- ✈️ Real Flights
- 🏨 Hotel Recommendations
- 🌦 Live Weather
- 💰 Budget Planning
- 🧠 AI Travel Suggestions
""")
    # ============================================
    # TRAVEL PLANNER TAB
    # ============================================

    with gr.Tab("✈️ Travel Planner"):

        with gr.Row(): 
            username = gr.Textbox(
                label="👤 Username",
                placeholder="Enter your name"
            )

            source = gr.Textbox(
                label="🛫 Source City",
                placeholder="e.g. Mumbai"
            )

            destination = gr.Textbox(
                label="📍 Destination City",
                placeholder="e.g. Goa"
            )

        with gr.Row():
            days = gr.Slider(
                minimum=1,
                maximum=15,
                value=3,
                step=1,
                label="📅 Number of Days"
            )

            budget = gr.Number(
                label="💰 Total Budget (₹)",
                value=20000
            )

        interests = gr.Textbox(
            label="🎯 Interests",
            placeholder="e.g. beaches, food, adventure"
        )

        with gr.Row():
            generate = gr.Button(
                "🚀 Generate Travel Plan",
                variant="primary",
                scale=2
            )
            
            pdf_btn = gr.Button(
                "📄 Download PDF",
                variant="secondary",
                scale=1
            )
            
            map_btn = gr.Button(
                "🗺️ Generate Map",
                variant="secondary",
                scale=1
            )

        output = gr.Textbox(
            label="📋 Travel Plan",
            lines=25
        )

        with gr.Row():
            pdf_output = gr.File(label="Travel Plan PDF")
            map_output = gr.File(label="Interactive Map")

    generate.click(
    fn=travel_planner,
    inputs=[
        username,
        source,
        destination,
        days,
        budget,
        interests
    ],
    outputs=output
    )   

    pdf_btn.click(
    fn=generate_trip_pdf,
    inputs=[
        username,
        source,
        destination,
        days,
        budget,
        interests
    ],
    outputs=pdf_output
    ) 

    map_btn.click(
    fn=generate_map_async,
    inputs=[destination],
    outputs=map_output
    )

    # ============================================
    # CHATBOT TAB
    # ============================================

    with gr.Tab("🤖 AI Travel Chatbot"):

        chatbot_ui = gr.Chatbot(
            label="Travel Assistant",
            height=450
        )

        with gr.Row():

            msg = gr.Textbox(
                placeholder="Ask about travel...",
                scale=4
            )

            send_btn = gr.Button(
                "Send",
                scale=1
            )

        clear_btn = gr.Button(
            "🗑️ Clear Chat"
        )

        msg.submit(
            chatbot,
            [msg, chatbot_ui],
            [msg, chatbot_ui]
        )

        send_btn.click(
            chatbot,
            [msg, chatbot_ui],
            [msg, chatbot_ui]
        )

        clear_btn.click(
            fn=lambda: ([], ""),
            inputs=None,
            outputs=[chatbot_ui, msg]
        )



# ============================================
# RUN APP
# ============================================

if __name__ == "__main__":

    app.launch(
        share=False,
        show_error=True,
        theme=gr.themes.Soft(),
        css=css_code
    )