import os
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

app = Flask(__name__)


@app.route("/")
def main():
    return {"hello": "world!"}


@app.route("/user")
def user():
    return {"name": "main"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
