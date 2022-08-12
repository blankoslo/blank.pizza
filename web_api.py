#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, Response
from flask_cors import cross_origin
#import requests
import json
#import api
import db
app = Flask(__name__)


@app.route("/api/action", methods=['GET', 'POST'])
def action():
    payload = json.loads(request.form["payload"])
    # team_id = requestDict['team']['id']
    responses = []
    response_url = payload['response_url']

    for action in payload['actions']:
        responses.append(button_rsvp(
            payload['user']['id'], action['value'], payload['original_message'], response_url))

    return '', 200

@app.route("/api/events", methods=['GET', 'POST'])
@cross_origin()
def events():
    if request.method == 'GET':
        raw_events = db.get_previous_pizza_events()
        events = [{"time": a[0], "place":a[1], "attendees":a[2].split(', ')} for a in raw_events]
        return events
    else:
        event = request.json['event']
        db.create_new_pizza_event(convert_datetime_object_to_timestamp(event['time']), place)
        return '', 201

def convert_datetime_object_to_timestamp(date):
    months={"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    strings = date.split()
    timestamp = f"{strings[3]}{months[strings[1]]}{strings[2]} {strings[4]} GMT"
    return timestamp


def button_rsvp(user_id, rsvp, original_message, response_url):
    if user_id in api.get_invited_users():
        api.rsvp(user_id, rsvp)
        if(rsvp == "attending"):
            api.finalize_event_if_complete()
            response_JSON = response_message(
                original_message, "✅ Sweet! Det blir sykt nice! 😋")
            requests.post(response_url, response_JSON)
        elif (rsvp == "not attending"):
            api.invite_if_needed()
            response_JSON = response_message(
                original_message, "⛔️ Ah, ok. Neste gang! 🤝")
            requests.post(response_url, response_JSON)
    else:
        response_JSON = response_message(
            original_message, "💣 Hmm, hva har du gjort for noe rart nå?")
        requests.post(response_url, response_JSON)


def response_message(original_message, text):
    original_message['attachments'] = [{'text': text}]
    return json.dumps(original_message)

app.run(host="0.0.0.0",port=8080)
