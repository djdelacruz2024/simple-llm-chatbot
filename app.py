import os

from flask import Flask, jsonify, render_template, request
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    if not os.getenv("OPENAI_API_KEY"):
        return jsonify({"error": "OPENAI_API_KEY is not set."}), 500

    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "You are a helpful, concise chatbot."},
                {"role": "user", "content": message},
            ],
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(debug=True)
