import type { Context } from '@netlify/functions'
import Anthropic from '@anthropic-ai/sdk'

const anthropic = new Anthropic()

export default async (req: Request, _context: Context) => {
  if (req.method !== 'POST') {
    return new Response('Method not allowed', { status: 405 })
  }

  const { message } = await req.json()

  if (!message) {
    return Response.json({ error: 'Message is required.' }, { status: 400 })
  }

  const response = await anthropic.messages.create({
    model: 'claude-haiku-4-5',
    max_tokens: 1024,
    system:
      'You are a helpful AI travel assistant. Answer questions about travel destinations, tips, itineraries, and advice. Be concise, friendly, and helpful.',
    messages: [{ role: 'user', content: message }],
  })

  const text =
    response.content[0].type === 'text'
      ? response.content[0].text
      : "I couldn't process that request."

  return Response.json({ response: text })
}

export const config = {
  path: '/api/chatbot',
}
