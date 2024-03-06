from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/send-data", methods=["POST"])
def handle_data():
    data = request.json
    print(data)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
