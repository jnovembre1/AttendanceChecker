from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(message=f"flask running, here's the db test: {os.getenv('POSTGRES_USER', 'unknown')}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
