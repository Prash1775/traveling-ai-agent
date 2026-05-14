# 🌍 Traveling AI Agent

An AI-powered smart travel planner that helps users organize their trips by providing real-time flight info, hotel recommendations, local weather, and custom day-by-day itineraries.

## 🚀 Features
- **✈️ Flight Search**: Find real flights with pricing and timing.
- **🏨 Hotel Recommendations**: Get top-rated hotels at your destination.
- **🌦️ Live Weather**: Check the current weather conditions.
- **📅 AI Itinerary**: Generate a complete day-by-day travel plan using Ollama (Llama 3).
- **💰 Budget Tracker**: Calculate expenses and see remaining budget.
- **📄 PDF Export**: Download your travel plan as a professional PDF.
- **🗺️ Interactive Map**: View your destination on an interactive map.

## 🛠️ Tech Stack
- **Backend**: Python, Asyncio
- **UI**: Gradio
- **AI Models**: Ollama (Llama 3), Google Gemini
- **Libraries**: Folium, Geopy, FPDF, Requests

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/traveling-ai-agent.git
   cd traveling-ai-agent
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up API Keys**:
   - Rename `utils/api_keys_template.py` to `utils/api_keys.py`.
   - Add your API keys for Google Gemini, OpenWeatherMap, RapidAPI, etc.

5. **Run Ollama**:
   - Make sure Ollama is installed and running.
   - Pull the model: `ollama pull llama3`

6. **Start the App**:
   ```bash
   python app.py
   ```

## 📝 License
MIT License
