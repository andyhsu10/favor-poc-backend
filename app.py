from flask import Flask, jsonify, request
from flask_cors import CORS

from utils.crawler import Crawler
from utils.openai import get_matching_result

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

@app.route("/matchings")
def get_tutor_matchings():
    description = request.args.get("description", default="", type=str)
    if not description:
        return jsonify({
            "data": []
        })

    tutor_results = Crawler(
        url="https://www.teaching.com.tw/member/case-list.php",
    ).run()
    tutors = [result for result in tutor_results if "高" in result["student"]]
    matching_str = get_matching_result(tutors, description)
    matching_ids = [word.strip() for word in matching_str.split("\n")]
    results = [result for result in tutor_results if result["id"] in matching_ids]
    return jsonify({
            "data": results
        })

if __name__ == "__main__":
    app.run(host="localhost", port=8080)
