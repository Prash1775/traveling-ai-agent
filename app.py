import streamlit as st
import asyncio
import os
from streamlit_folium import st_folium

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
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Traveling AI Agent",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================
# STYLING
# ============================================
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    .report-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #1e2130;
        border: 1px solid #3e4259;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================
# HELPER FUNCTIONS
# ============================================

async def get_travel_data(source, destination, days, interests):
    tasks = [
        asyncio.to_thread(get_weather, destination),
        asyncio.to_thread(search_hotels, destination),
        asyncio.to_thread(search_flights, source, destination),
        asyncio.to_thread(get_combined_travel_data, destination, days, interests)
    ]
    return await asyncio.gather(*tasks, return_exceptions=True)

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/travel-pro.png")
    st.title("Settings")
    username = st.text_input("👤 Username", placeholder="Enter your name", value="Traveler")
    source = st.text_input("🛫 Source City", placeholder="e.g. Mumbai")
    destination = st.text_input("📍 Destination City", placeholder="e.g. Goa")
    
    st.divider()
    days = st.slider("📅 Number of Days", 1, 15, 3)
    budget_input = st.text_input("💰 Total Budget (₹)", value="20000")
    try:
        budget = int(budget_input.replace(",", ""))
    except:
        budget = 20000
    interests = st.text_area("🎯 Interests", placeholder="e.g. beaches, food, adventure")

# ============================================
# MAIN UI
# ============================================
st.title("🌍 Traveling AI Agent")
st.caption("AI Powered Smart Travel Planner - Built with Gemini & Groq")

tab1, tab2 = st.tabs(["✈️ Travel Planner", "🤖 AI Chatbot"])

# ============================================
# TAB 1: TRAVEL PLANNER
# ============================================
with tab1:
    if st.button("🚀 Generate Complete Travel Plan"):
        if not source or not destination:
            st.warning("⚠️ Please enter both Source and Destination in the sidebar.")
        else:
            with st.spinner("🚢 Planning your trip..."):
                # Save to memory
                save_memory(username, {"destination": destination, "interests": interests, "budget": budget})
                
                # Run agents
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                results = loop.run_until_complete(get_travel_data(source, destination, days, interests))
                
                weather = results[0] if not isinstance(results[0], Exception) else "Weather unavailable"
                hotels = results[1] if not isinstance(results[1], Exception) else []
                flights = results[2] if not isinstance(results[2], Exception) else []
                ai_content = results[3] if not isinstance(results[3], Exception) else "No travel details available"

                # Process results
                hotel = hotels[0] if hotels else {"name": "Not Found", "price_per_night": 0}
                flight = flights[0] if flights else {"airline": "N/A", "price": 0, "time": "N/A"}
                
                budget_report = calculate_budget(budget, hotel.get("price_per_night", 0) * int(days), flight.get("price", 0))

                # ============================================
                # PREMIUM RESULTS DASHBOARD
                # ============================================
                st.markdown("### 📊 Your Trip Dashboard")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="report-card">
                        <h4>🌦️ Weather</h4>
                        <h2 style="color: #00d4ff;">{weather}</h2>
                        <p style="font-size: 0.8em; color: #888;">Condition & Temperature</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    hotel_name = hotel.get("name", "Not Found")
                    st.markdown(f"""
                    <div class="report-card">
                        <h4>🏨 Top Hotel</h4>
                        <h2 style="color: #ffaa00;">{hotel_name[:15]}...</h2>
                        <p style="font-size: 0.8em; color: #888;">₹{hotel.get('price_per_night', 0):,} per night</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.markdown(f"""
                    <div class="report-card">
                        <h4>💰 Remaining</h4>
                        <h2 style="color: #4CAF50;">₹{budget_report['remaining']:,}</h2>
                        <p style="font-size: 0.8em; color: #888;">From total budget</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.divider()

                # Detailed Sections
                c1, c2 = st.columns([1, 1])

                with c1:
                    st.markdown("#### ✈️ Flight Options")
                    if flights:
                        for f in flights[:2]:
                            with st.container(border=True):
                                st.write(f"**{f.get('airline')}**")
                                st.write(f"🕒 {f.get('time')} | 🏷️ ₹{f.get('price', 0):,}")
                                st.button(f"Book {f.get('airline')}", key=f"btn_{f.get('airline')}_{f.get('price')}")
                    else:
                        st.info("No flights found for this route.")

                with c2:
                    st.markdown("#### 🏨 Hotel Details")
                    if hotels:
                        for h in hotels[:2]:
                            with st.container(border=True):
                                st.write(f"**{h.get('name')}**")
                                st.write(f"⭐ {h.get('stars')} Stars | 🏷️ ₹{h.get('price_per_night', 0):,}")
                                st.link_button("View on Booking.com", h.get("booking_link", "https://www.booking.com"))
                    else:
                        st.info("No hotels found in this city.")

                st.divider()
                
                # Full Itinerary
                st.markdown(f"### 📅 {days}-Day Itinerary & Recommendations")
                st.markdown(f"""
                <div style="background-color: #1e2130; padding: 25px; border-radius: 15px; border: 1px solid #3e4259;">
                    {ai_content}
                </div>
                """, unsafe_allow_html=True)
                
                st.divider()
                
                # Download and Map
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("#### 📄 Export Plan")
                    report_text = f"Destination: {destination}\nWeather: {weather}\nHotel: {hotel.get('name')}\nBudget Status: {budget_report['remaining']}\n\n{ai_content}"
                    pdf_path = generate_pdf(report_text)
                    with open(pdf_path, "rb") as f:
                        st.download_button("Download PDF Report", f, file_name="travel_plan.pdf")
                
                with col_b:
                    st.markdown("#### 🗺️ Interactive Map")
                    map_path = generate_map(destination)
                    if map_path:
                        st.success("Map Generated! (See below)")

                # Display Map if exists
                if map_path and os.path.exists(map_path):
                    with open(map_path, 'r', encoding='utf-8') as f:
                        st.components.v1.html(f.read(), height=500)

# ============================================
# TAB 2: CHATBOT
# ============================================
with tab2:
    st.markdown("### 🤖 Travel Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me about your trip..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = ask_ai(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()
st.markdown("<center><b>🤖 POWERED BY GOOGLE GEMINI & GROQ</b></center>", unsafe_allow_html=True)