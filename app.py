from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".", static_url_path="")

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    # Your Python logic here
    answer = f"You asked: {question}"

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)