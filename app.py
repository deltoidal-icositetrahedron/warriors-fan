from flask import Flask, request, jsonify, render_template
from process_question import process

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")

    response = process(user_message)

    return jsonify({
        "reply": response.content[0].text
    })

if __name__ == "__main__":
    app.run(debug=True)