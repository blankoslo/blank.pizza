from flask import Flask, request
from urllib.parse import unquote_plus
import json
import re
app = Flask(__name__)


def parse_request(request):
    """
    Parse the Slack POST request.
    """
    payload = request.get_data()
    payload = unquote_plus(payload)
    payload = re.sub('payload=', '', payload)
    payload = json.loads(payload)
    return payload


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/api/action", methods=['GET', 'POST'])
def action():
    payload = parse_request(request)
    print(payload)
    return 'Jabba'
