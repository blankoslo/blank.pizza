from flask import Flask, request
import json
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/api/action", methods=['GET', 'POST'])
def action():
    # requestDict = json.loads(request.data.decode("utf-8"))
    print(type(request.data))
    print(request.data)

    # print(requestDict)
    # team_id = requestDict['team']['id']
    # user_id = requestDict['user']['id']
    return 'Jabba'
