from flask import Flask, request
import json
import api
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/api/action", methods=['GET', 'POST'])
def action():
    payload = json.loads(request.form["payload"])
    # team_id = requestDict['team']['id']

    for action in payload['actions']:
        button_rsvp(payload['user']['id'], action['value'])


def button_rsvp(user_id, rsvp):
    if user_id in api.get_invited_users():
        api.rsvp(user_id, rsvp)
        if(rsvp == "attending"):
            api.finalize_event_if_complete()
            return "Sweet! Det blir sykt nice 😋"
        elif (rsvp == "not attending"):
            api.invite_if_needed()
            return "Ah, ok. Neste gang! 🤝"
    else:
        return "Hmm, hva har du gjort for noe rart nå?"
