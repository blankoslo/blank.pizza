#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, Response
import requests
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
    response_url = payload['response_url']

    for action in payload['actions']:
        responses.append(button_rsvp(
            payload['user']['id'], action['value'], payload['original_message'], response_url))

    return Response(response=responses[0], mimetype='application/json')


def button_rsvp(user_id, rsvp, original_message, response_url):
    print(response_url)
    if user_id in api.get_invited_users():
        api.rsvp(user_id, rsvp)
        if(rsvp == "attending"):
            api.finalize_event_if_complete()
            response_JSON = response_message(
                original_message, "✅ Sweet! Det blir sykt nice! 😋")
            requests.post(response_url, json=response_JSON)
        elif (rsvp == "not attending"):
            api.invite_if_needed()
            response_JSON = response_message(
                original_message, "⛔️ Ah, ok. Neste gang! 🤝")
            requests.post(response_url, json=response_JSON)
    else:
        response_JSON = response_message(
            original_message, "💣 Hmm, hva har du gjort for noe rart nå?")
        requests.post(response_url, json=response_JSON)


def response_message(original_message, text):
    original_message['attachments'] = [{'text': text}]
    print(json.dumps(original_message))

    return json.dumps(original_message)
