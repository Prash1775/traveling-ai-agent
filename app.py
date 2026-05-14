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
)

# ============================================
# STYLING (MOBILE FRIENDLY & HIGH CONTRAST)
# ============================================
st.markdown("""
    <style>
    .report-card {
        padding: 20px;
        border-radius: 12px;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        color: #212529;
        margin-bottom: 10px;
    }
    .itinerary-box {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #dee2e6;
        color: #212529;
        line-height: 1.6;
    }
    h1, h2, h3 {
        color: #1a73e8;
    }
    .stButton>button {
        background-color: #1a73e8;
        color: white;
        border-radius: 8px;
        height: 3.5em;
        font-weight: bold;
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
# MAIN UI
# ============================================
st.title("🌍 Traveling AI Agent")
st.caption("Professional Smart Travel Planner")

# TOP INPUT SECTION (Instead of Sidebar)
with st.container(border=True):
    st.markdown("### 🛫 Plan Your Trip")
    r1_c1, r1_c2, r1_c3 = st.columns(3)
    with r1_c1:
        username = st.text_input("👤 Your Name", value="Traveler")
    with r1_c2:
        source = st.text_input("🛫 Source City", placeholder="e.g. Mumbai")
    with r1_c3:
        destination = st.text_input("📍 Destination City", placeholder="e.g. Goa")

    r2_c1, r2_c2, r2_c3 = st.columns(3)
    with r2_c1:
        days = st.slider("📅 Days", 1, 15, 3)
    with r2_c2:
        budget_input = st.text_input("💰 Total Budget (₹)", value="20000")
        try:
            budget = int(budget_input.replace(",", ""))
        except:
            budget = 20000
    with r2_c3:
        interests = st.text_input("🎯 Interests", placeholder="beaches, food, adventure")

tab1, tab2 = st.tabs(["✈️ Travel Planner", "🤖 AI Chatbot"])

# ============================================
# TAB 1: TRAVEL PLANNER
# ============================================
with tab1:
    if st.button("🚀 Generate Complete Travel Plan"):
        if not source or not destination:
            st.warning("⚠️ Please enter both Source and Destination above.")
        else:
            with st.spinner("🚢 Planning your trip..."):
                save_memory(username, {"destination": destination, "interests": interests, "budget": budget})
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                results = loop.run_until_complete(get_travel_data(source, destination, days, interests))
                
                weather = results[0] if not isinstance(results[0], Exception) else "Unavailable"
                hotels = results[1] if not isinstance(results[1], Exception) else []
                flights = results[2] if not isinstance(results[2], Exception) else []
                ai_content = results[3] if not isinstance(results[3], Exception) else f"Error: {results[3]}"

                # RESULTS DASHBOARD
                st.markdown("### 📊 Trip Summary")
                d_c1, d_c2, d_c3 = st.columns(3)
                
                with d_c1:
                    st.markdown(f'<div class="report-card"><h4>🌦️ Weather</h4><h2>{weather}</h2></div>', unsafe_allow_html=True)
                with d_c2:
                    hotel_name = hotels[0].get("name", "Not Found") if hotels else "Not Found"
                    st.markdown(f'<div class="report-card"><h4>🏨 Stay</h4><h2>{hotel_name[:15]}...</h2></div>', unsafe_allow_html=True)
                with d_c3:
                    hotel_cost = hotels[0].get("price_per_night", 0) if hotels else 0
                    flight_cost = flights[0].get("price", 0) if flights else 0
                    rem = budget - (hotel_cost * days + flight_cost)
                    st.markdown(f'<div class="report-card"><h4>💰 Left</h4><h2 style="color: green;">₹{rem:,}</h2></div>', unsafe_allow_html=True)

                st.divider()

                # Detailed Sections
                s1, s2 = st.columns(2)
                with s1:
                    st.markdown("#### ✈️ Flights")
                    if flights:
                        for f in flights[:2]:
                            with st.container(border=True):
                                st.write(f"**{f.get('airline')}** | ₹{f.get('price', 0):,} | {f.get('time')}")
                    else: st.info("No flights found.")

                with s2:
                    st.markdown("#### 🏨 Hotels")
                    if hotels:
                        for h in hotels[:2]:
                            with st.container(border=True):
                                st.write(f"**{h.get('name')}** | ⭐ {h.get('stars')} | ₹{h.get('price_per_night', 0):,}")
                    else: st.info("No hotels found.")

                st.divider()
                
                # Full Itinerary
                st.markdown(f"### 📅 {days}-Day Itinerary")
                st.markdown(f'<div class="itinerary-box">{ai_content}</div>', unsafe_allow_html=True)
                
                st.divider()
                
                # Map & PDF
                m1, m2 = st.columns(2)
                with m1:
                    pdf_path = generate_pdf(ai_content)
                    with open(pdf_path, "rb") as f:
                        st.download_button("📥 Download PDF Report", f, file_name="travel_plan.pdf")
                with m2:
                    map_obj = generate_map(destination)
                    if map_obj: st.success("Map Ready!")

                if map_obj:
                    st.divider()
                    st.markdown("#### 🗺️ Interactive Destination Map")
                    # The most reliable way to show folium on cloud:
                    map_html = map_obj._repr_html_()
                    st.components.v1.html(map_html, height=500, scrolling=True)

# ============================================
# TAB 2: CHATBOT
# ============================================
with tab2:
    st.markdown("### 🤖 Travel Assistant")
    if "messages" not in st.session_state: st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]): st.markdown(message["content"])
    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            response = ask_ai(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown("<center><small>Powered by Gemini & Groq</small></center>", unsafe_allow_html=True)