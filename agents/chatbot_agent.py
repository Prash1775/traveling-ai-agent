from groq import Groq

from utils.api_keys import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

def ask_ai(prompt):

    try:

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Groq Error: {str(e)}"