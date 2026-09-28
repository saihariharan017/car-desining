import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-3.1-flash-lite"

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=API_KEY)

with open("chatbot_config.txt", "r", encoding="utf-8") as file:
    SYSTEM_PROMPT = file.read().strip()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    try:
        prompt = f"{SYSTEM_PROMPT}\n\nUser question:\n{message}"

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        answer = response.text.strip() if response.text else (
            "I couldn't generate a response. Please try again."
        )

        return jsonify({"answer": answer})

    except Exception:
        return jsonify({
            "error": "The chatbot could not process your request right now."
        }), 500


if __name__ == "__main__":
    app.run()
