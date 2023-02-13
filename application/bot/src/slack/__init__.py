import requests
import base64
import logging
import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from src.api.bot_api import BotApi, BotApiConfiguration

from src.injector import injector

pizza_channel_id = os.environ["PIZZA_CHANNEL_ID"]
slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_app_token = os.environ["SLACK_APP_TOKEN"]

slack_app = App(token=slack_bot_token)
slack_handler = SocketModeHandler(slack_app, slack_app_token)

@slack_app.event("message")
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

def handle_rsvp(body, ack, attending):
    user = body["user"]
    user_id = user["id"]
    channel = body["channel"]
    channel_id = channel["id"]
    message = body["message"]
    with injector.get(BotApi) as ba:
        invited_users = ba.get_invited_users()
        if user_id in invited_users:
            ts = message['ts']
            event_id = body["actions"][0]["value"]
            blocks = message["blocks"][0:3]
            if attending:
                ba.accept_invitation(event_id, user_id)
            else:
                ba.decline_invitation(event_id, user_id)
                ba.invite_multiple_if_needed()
            ba.send_pizza_invite_answered(channel_id, ts, event_id, blocks, attending)
    ack()

@slack_app.action("rsvp_yes")
def handle_rsvp_yes(ack, body):
    handle_rsvp(body, ack, True)

@slack_app.action("rsvp_no")
def handle_rsvp_no(ack, body):
    handle_rsvp(body, ack, False)

@slack_app.action("rsvp_withdraw")
def handle_rsvp_withdraw(ack, body):
    logger = injector.get(logging.Logger)
    message = body["message"]
    user = body["user"]
    user_id = user["id"]
    channel = body["channel"]
    channel_id = channel["id"]
    event_id = body["actions"][0]["value"]
    ts = message['ts']
    blocks = message["blocks"][0:3]
    with injector.get(BotApi) as ba:
        success = ba.withdraw_invitation(event_id, user_id)
        if success:
            logger.info("%s withdrew their invitation", user_id)
            ba.send_pizza_invite_withdraw(channel_id, ts, blocks)
        else:
            logger.warning("failed to withdraw invitation for %s", user_id)
            ba.send_pizza_invite_withdraw_failure(channel_id, ts, blocks)
    ack()

# We don't use channel messages, but perhaps it'll be useful in the future
def handle_channel_message(event, say):
    logger = injector.get(logging.Logger)
    logger.info(event)

# We don't use direct messages, but perhaps it'll be useful in the future
def handle_direct_message(event, say):
    logger = injector.get(logging.Logger)
    logger.info(event)

# We don't use app mentions at the moment, but perhaps it'll be useful in the future
@slack_app.event("app_mention")
def handle_mention_event(body):
    logger = injector.get(logging.Logger)
    logger.info(body)

def handle_file_share(event, say):
    channel = event["channel"]
    if 'files' in event:
        files = event['files']
        with injector.get(BotApi) as ba:
            ba.send_slack_message_old(channel, u'Takk for fil! 🤙')
            headers = {u'Authorization': u'Bearer %s' % slack_bot_token}
            for file in files:
                r = requests.get(
                    file['url_private'], headers=headers)
                b64 = base64.b64encode(r.content).decode('utf-8')
                payload = {'file': 'data:image;base64,%s' % b64,
                           'upload_preset': 'blank.pizza'}
                r2 = requests.post(
                    'https://api.cloudinary.com/v1_1/blank/image/upload', data=payload)
                ba.save_image(
                    r2.json()['public_id'], file['user'], file['title'])

# This only exists to make bolt not throw a warning that we dont handle the file_shared event
# We dont use this as we use the message event with subtype file_shared as that one
# contains a full file object with url_private, while this one only contains the ID
# Perhaps another file event contains the full object?
@slack_app.event("file_shared")
def handle_file_shared_events(body):
    logger = injector.get(logging.Logger)
    logger.info(body)