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
def handle_event(body, say, logger):
    event = body["event"]
    channel = event["channel"]
    channel_type = event["channel_type"]
    # Handle a channel message in the pizza channel
    if "subtype" not in event and channel_type == 'channel' and channel == pizza_channel_id:
        handle_channel_message(event, say, logger)
    # Handle a direct message to bot
    elif "subtype" not in event and channel_type == 'im':
        handle_direct_message(event, say, logger)
    # Handle a file share
    elif "subtype" in event and event["subtype"] == 'file_share':
        handle_file_share(event, say)

def handle_rsvp(body, ack, attending):
    user = body["user"]
    user_id = user["id"]
    channel = body["channel"]
    channel_id = channel["id"]
    message = body["message"]
    if user_id in api.get_invited_users():
        ts = message['ts']
        blocks = message["blocks"]
        actions_blocks = blocks[3]
        event_id = actions_blocks["elements"][0]["value"]
        rest_blocks = blocks[0:3]
        api.rsvp(user_id, RSVP.attending)
        api.send_pizza_invite_answered(channel_id, ts, event_id, rest_blocks, attending)
        api.invite_if_needed()
    ack()

@app.action("rsvp_yes")
def handle_rsvp_yes(ack, body):
    handle_rsvp(body, ack, True)

@app.action("rsvp_no")
def handle_rsvp_no(ack, body):
    handle_rsvp(body, ack, False)

@app.action("rsvp_withdraw")
def handle_some_action(ack, body):
    message = body["message"]
    blocks = message["blocks"]
    accessory_block = blocks[5]["accessory"]
    event_id = accessory_block["value"]
    print(event_id)
    ack()

# We don't use channel messages, but perhaps it'll be useful in the future
def handle_channel_message(event, say, logger):
    logger.info(event)

# We don't use direct messages, but perhaps it'll be useful in the future
def handle_direct_message(event, say, logger):
    logger.info(event)

# We don't use app mentions at the moment, but perhaps it'll be useful in the future
@app.event("app_mention")
def handle_mention_event(body, logger):
    logger.info(body)

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

if __name__ == "__main__":
    handler = SocketModeHandler(app, slack_app_token)
    handler.start()