from flask import Flask, request, jsonify, render_template
from process_question import process
from pathlib import Path
import json
import time

app = Flask(__name__)

LOG_FILE = Path("chat_log.jsonl")
MEMORY_LENGTH = 100

def clear_log_on_start():
    LOG_FILE.write_text("", encoding="utf-8")

def save_message(role, text):
    record = {
        "time": time.time(),
        "role": role,
        "text": text
    }
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def load_recent_messages(n=MEMORY_LENGTH):
    if not LOG_FILE.exists():
        return []

    messages = []
    with LOG_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                messages.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return messages[-n:]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True, silent=True) or {}
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # load memory FIRST (so we don't duplicate the new user message in history)
    history = load_recent_messages()

    # save user message
    save_message("user", user_message)

    response = process(user_message, history)
    reply = response.content[0].text

    # save assistant reply (Anthropic role name)
    save_message("assistant", reply)

    return jsonify({"reply": reply})

@app.route("/reset", methods=["POST"])
def reset():
    LOG_FILE.write_text("", encoding="utf-8")
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    clear_log_on_start()
    app.run(host="127.0.0.1", port=5000, debug=True)
