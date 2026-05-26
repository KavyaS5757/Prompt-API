from flask import Flask, request, jsonify, send_from_directory
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def index():
    return send_from_directory("public", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    messages = request.json.get("messages", [])
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, *messages]
    )
    return jsonify({"reply": response.choices[0].message.content})

if __name__ == "__main__":
    print("🌐 Web chatbot at http://localhost:3000")
    app.run(port=3000, debug=True)