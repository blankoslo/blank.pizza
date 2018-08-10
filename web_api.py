#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, Response
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
    responses = []

    for action in payload['actions']:
        responses.append(button_rsvp(
            payload['user']['id'], action['value'], payload['original_message']))

    return Response(response=responses[0], mimetype='application/json')


def button_rsvp(user_id, rsvp, original_message):
    if user_id in api.get_invited_users():
        api.rsvp(user_id, rsvp)
        if(rsvp == "attending"):
            api.finalize_event_if_complete()
            return response_message(original_message, "Sweet! Det blir sykt nice 😋")
        elif (rsvp == "not attending"):
            api.invite_if_needed()
            return response_message(original_message, "Ah, ok. Neste gang! 🤝")
    else:
        return response_message(original_message, "Hmm, hva har du gjort for noe rart nå?")


def response_message(original_message, text):
    original_message['attachments'] = []
    original_message['text'] = text
    original_message['replace_original'] = False

    return json.dumps(original_message)
