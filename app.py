import logging
import os

from flask import Flask, jsonify, render_template, request
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = "You are a helpful, concise chatbot."
# How many previous messages (user + assistant) to send along for context.
MAX_HISTORY_MESSAGES = 20
MAX_MESSAGE_LENGTH = 4000

_client = None


def get_client():
    """Create the OpenAI client on first use so the app can start without a key."""
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client


def clean_history(history):
    """Keep only well-formed user/assistant turns from the client-supplied history."""
    if not isinstance(history, list):
        return []

    cleaned = []
    for item in history[-MAX_HISTORY_MESSAGES:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content")
        if role in ("user", "assistant") and isinstance(content, str) and content.strip():
            cleaned.append({"role": role, "content": content[:MAX_MESSAGE_LENGTH]})
    return cleaned


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    if len(message) > MAX_MESSAGE_LENGTH:
        return jsonify({"error": f"Messages are limited to {MAX_MESSAGE_LENGTH} characters."}), 400

    if not os.getenv("OPENAI_API_KEY"):
        return jsonify({"error": "OPENAI_API_KEY is not set. Add it to your .env file and restart the server."}), 500

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *clean_history(data.get("history")),
        {"role": "user", "content": message},
    ]

    try:
        response = get_client().chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=messages,
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except OpenAIError as exc:
        logger.exception("OpenAI request failed")
        return jsonify({"error": f"The model request failed: {exc}"}), 502


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
