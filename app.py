from flask import Flask, jsonify
from flask_cors import CORS

from utils.crawler import Crawler

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/.*": {
            "origins": ["http://localhost:3000"]
        }
    }
)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/tutors")
def get_tutors():
    results = Crawler(
        url="https://www.teaching.com.tw/member/case-list.php",
    ).run()
    return jsonify({
        "data": results
    })

if __name__ == "__main__":
    app.run(host="localhost", port=8080)
