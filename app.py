from flask import Flask, jsonify

from utils.crawler import Crawler

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/tutors")
def get_tutors():
    results = Crawler(
        url="https://www.teaching.com.tw/member/case-list.php",
    ).run()
    return jsonify(results)

if __name__ == "__main__":
    app.run()
