from flask import Flask, request
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/api/action")
def action():
    app.logger.info(request.json)
    return "Hello"
