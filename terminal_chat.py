from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
history = []

print('🤖 Terminal Chatbot ready! Type "exit" to quit.\n')

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, *history]
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})

    print(f"\nAI: {reply}\n")