from flask import Flask, request
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/api/action", methods=['GET', 'POST'])
def action():
    print(request.is_json)
    content = request.get_json()
    print(content)
    return 'JSON posted'
