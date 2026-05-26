from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 📄 Change this to any text you want to query against!
KNOWLEDGE = """
The Eiffel Tower is located in Paris, France. It was built in 1889
by Gustave Eiffel for the World's Fair. It stands 330 meters tall.
About 7 million people visit it each year. The tower was almost
demolished in 1909 but was saved because it served as a radio tower.
"""

print("📚 Q&A App ready! Ask questions about the document.")
print('Type "exit" to quit.\n')

while True:
    question = input("Your question: ")
    if question.lower() == "exit":
        break

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""You are a helpful assistant. Answer questions ONLY based on this document:

{KNOWLEDGE}

If the answer isn't in the document, say "I don't have that information."
Keep answers concise and factual."""
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    print(f"\nAnswer: {response.choices[0].message.content}\n")