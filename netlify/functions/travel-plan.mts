import type { Context } from '@netlify/functions'
import Anthropic from '@anthropic-ai/sdk'

const MOCK_HOTELS = [
  { name: 'Grand Palace Hotel', stars: 5, price_per_night: 5000, booking_link: 'https://www.booking.com' },
  { name: 'City Comfort Inn', stars: 3, price_per_night: 2500, booking_link: 'https://www.booking.com' },
  { name: 'Budget Stay Lodge', stars: 2, price_per_night: 1200, booking_link: 'https://www.booking.com' },
]

const MOCK_FLIGHTS = [
  { airline: 'IndiGo', price: 4500, time: '09:00 AM', booking_link: 'https://www.skyscanner.com' },
  { airline: 'Air India', price: 5200, time: '12:30 PM', booking_link: 'https://www.skyscanner.com' },
  { airline: 'SpiceJet', price: 3900, time: '06:45 PM', booking_link: 'https://www.skyscanner.com' },
]

async function getWeather(city: string): Promise<string> {
  const apiKey = process.env.WEATHER_API_KEY
  if (!apiKey || apiKey === 'YOUR_OPENWEATHERMAP_API_KEY_HERE') {
    return 'Clear sky, 28°C'
  }
  try {
    const res = await fetch(
      `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&appid=${apiKey}&units=metric`,
      { signal: AbortSignal.timeout(5000) }
    )
    const data = await res.json()
    if (!data.weather) return 'Weather unavailable'
    return `${data.weather[0].description}, ${data.main.temp}°C`
  } catch {
    return 'Weather unavailable'
  }
}

async function getAIContent(destination: string, days: number, interests: string): Promise<string> {
  const anthropic = new Anthropic()
  const message = await anthropic.messages.create({
    model: 'claude-haiku-4-5',
    max_tokens: 2048,
    messages: [
      {
        role: 'user',
        content: `You are an expert travel guide. Create a complete travel plan for ${destination} for ${days} days.
The traveler's interests are: ${interests}

Please provide a response with the following structured sections:

1. 🎯 RECOMMENDATIONS
   - 🏛️ Top Tourist Places
   - 🍽️ Best Restaurants & Local Food
   - ☕ Popular Cafes
   - 🎯 Must-try Activities & Experiences

2. 📅 DAY-BY-DAY ITINERARY
   For each of the ${days} days, provide:
   - 🌅 Morning: Activity
   - ☀️ Afternoon: Activity & Lunch spot
   - 🌙 Evening: Activity & Dinner spot

Keep the tone professional and helpful.`,
      },
    ],
  })
  return message.content[0].type === 'text' ? message.content[0].text : 'AI content unavailable'
}

export default async (req: Request, _context: Context) => {
  if (req.method !== 'POST') {
    return new Response('Method not allowed', { status: 405 })
  }

  const { source, destination, days, budget, interests } = await req.json()

  if (!source || !destination) {
    return Response.json({ error: 'Please enter both Source and Destination.' }, { status: 400 })
  }

  const daysNum = parseInt(days) || 3
  const budgetNum = parseInt(budget) || 20000
  const interestsStr = interests || 'general sightseeing'

  const [weather, aiContent] = await Promise.all([
    getWeather(destination),
    getAIContent(destination, daysNum, interestsStr),
  ])

  const hotel = MOCK_HOTELS[0]
  const flight = MOCK_FLIGHTS[0]
  const hotelTotalCost = hotel.price_per_night * daysNum
  const totalExpense = hotelTotalCost + flight.price
  const remaining = budgetNum - totalExpense

  return Response.json({
    destination,
    source,
    days: daysNum,
    budget: budgetNum,
    weather,
    hotel,
    flight,
    budget_report: { expense: totalExpense, remaining },
    ai_content: aiContent,
  })
}

export const config = {
  path: '/api/travel-plan',
}
