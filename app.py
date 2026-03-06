from flask import Flask, request, jsonify, render_template
from process_question import process
import time

app = Flask(__name__)

MEMORY_LENGTH = 100

# global in-memory message history
CHAT_HISTORY = []


def load_recent_messages(n=MEMORY_LENGTH):
    return CHAT_HISTORY[-n:]


def save_message(role, text):
    CHAT_HISTORY.append({
        "time": time.time(),
        "role": role,
        "text": text
    })


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True, silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    history = load_recent_messages()

    response = process(user_message, history)
    reply = response.content[0].text

    save_message("user", user_message)
    save_message("assistant", reply)

    return jsonify({"reply": reply})


@app.route("/reset", methods=["POST"])
def reset():
    CHAT_HISTORY.clear()
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)