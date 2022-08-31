#!/usr/bin/env python
# -*- coding: utf-8 -*-
import src.api.bot_api as api
import requests
import base64
import os
from src.database.rsvp import RSVP

from time import sleep
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

pizza_channel_id = os.environ["PIZZA_CHANNEL_ID"]

slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_app_token = os.environ["SLACK_APP_TOKEN"]
app = App(token=slack_bot_token)

@app.event("message")
def handle_event(body, say):
    event = body["event"]
    channel = event["channel"]
    channel_type = event["channel_type"]
    # Handle a channel message in the pizza channel
    if "subtype" not in event and channel_type == 'channel' and channel == pizza_channel_id:
        handle_channel_message(event, say)
    # Handle a direct message to bot
    elif "subtype" not in event and channel_type == 'im':
        handle_direct_message(event, say)
    # Handle a file share
    elif "subtype" in event and event["subtype"] == 'file_share':
        handle_file_share(event, say)

@app.action("rsvp")
def handle_some_action(ack, body):
    user = body["user"]
    user_id = user["id"]
    answer = body["actions"][0]["value"]
    channel = body["channel"]
    channel_id = channel["id"]
    original_message = body["original_message"]
    if user_id in api.get_invited_users():
        ts = original_message['ts']
        original_text = original_message['text']
        answer = RSVP(answer)
        if answer == api.BUTTONS_ATTACHMENT_OPTION_YES:
            api.rsvp(user_id, RSVP.attending)
            api.update_slack_message(channel_id, ts, original_text, [{'text': u'Sweet! 🤙'}])
            api.finalize_event_if_complete()
        elif answer == api.BUTTONS_ATTACHMENT_OPTION_NO:
            api.rsvp(user_id, RSVP.not_attending)
            api.update_slack_message(channel_id, ts, original_text, [{'text': u'Ok 😏'}])
            api.invite_if_needed()
        else:
            api.send_slack_message(channel_id, u'Hehe jeg er litt dum, jeg. Skjønner jeg ikke helt hva du mener 😳. Kan du være med? (ja/nei)')
    ack()

# We don't use channel messages, but perhaps it'll be useful in the future
def handle_channel_message(event, logger):
    logger.info(event)

def handle_direct_message(event, say):
    user = event["user"]
    message = event["text"]
    channel = event["channel"]
    if user in api.get_invited_users():
        if message.lower() == 'ja':
            api.rsvp(user, 'attending')
            api.send_slack_message(channel, u'Sweet! 🤙')
            api.finalize_event_if_complete()
        elif message.lower() == 'nei':
            api.rsvp(user, 'not attending')
            api.send_slack_message(channel, u'Ok 😏')
            api.invite_if_needed()
        else:
            api.send_slack_message(channel, u'Hehe jeg er litt dum, jeg. Skjønner jeg ikke helt hva du mener 😳. Kan du være med? (ja/nei)')

def handle_file_share(event, say):
    channel = event["channel"]
    if 'files' in event:
        files = event['files']
        api.send_slack_message(channel, u'Takk for fil! 🤙')
        headers = {u'Authorization': u'Bearer %s' % slack_bot_token}
        for file in files:
            r = requests.get(
                file['url_private'], headers=headers)
            b64 = base64.b64encode(r.content).decode('utf-8')
            payload = {'file': 'data:image;base64,%s' % b64,
                        'upload_preset': 'blank.pizza'}
            r2 = requests.post(
                'https://api.cloudinary.com/v1_1/blank/image/upload', data=payload)
            api.save_image(
                r2.json()['public_id'], file['user'], file['title'])

# This only exists to make bolt not throw a warning that we dont handle the file_shared event
# We dont use this as we use the message event with subtype file_shared as that one
# contains a full file object with url_private, while this one only contains the ID
# Perhaps another file event contains the full object?
@app.event("file_shared")
def handle_file_shared_events(body, logger):
    logger.info(body)

# We don't use app mentions at the moment, but perhaps it'll be useful in the future
@app.event("app_mention")
def handle_mention_event(body, logger):
    logger.info(body)

if __name__ == "__main__":
    handler = SocketModeHandler(app, slack_app_token)
    handler.start()