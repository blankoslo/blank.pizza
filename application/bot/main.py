#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import base64
import os
import locale
import threading
import pytz
import logging
import sys

from src.api.bot_api import BotApi, BotApiConfiguration

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.injector import injector, singleton
from src.broker.amqp_connection import AmqpConnection
from src.broker.handlers import on_message

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

@app.action("rsvp_yes")
def handle_rsvp_yes(ack, body):
    handle_rsvp(body, ack, True)

@app.action("rsvp_no")
def handle_rsvp_no(ack, body):
    handle_rsvp(body, ack, False)

@app.action("rsvp_withdraw")
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
@app.event("app_mention")
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
@app.event("file_shared")
def handle_file_shared_events(body):
    logger = injector.get(logging.Logger)
    logger.info(body)

def auto_reply():
    logger = injector.get(logging.Logger)
    logger.info("Auto replying on scheduled task")
    with injector.get(BotApi) as ba:
        ba.auto_reply()

def invite_multiple_if_needed():
    logger = injector.get(logging.Logger)
    logger.info("Inviting multiple if need on scheduled task")
    with injector.get(BotApi) as ba:
        ba.invite_multiple_if_needed()

def send_reminders():
    logger = injector.get(logging.Logger)
    logger.info("Sending reminders on scheduled task")
    with injector.get(BotApi) as ba:
        ba.send_reminders()

def sync_db_with_slack_and_return_count():
    logger = injector.get(logging.Logger)
    logger.info("Syncing db with slack on scheduled task")
    with injector.get(BotApi) as ba:
        ba.sync_db_with_slack_and_return_count()

def main():
    # Set up injector
    api_config = BotApiConfiguration(pizza_channel_id, pytz.timezone('Europe/Oslo'))
    injector.binder.bind(BotApiConfiguration, to=api_config)

    # Set up logging
    logger = logging.getLogger(__name__)
    logging_handler = logging.StreamHandler(sys.stdout)
    logging_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
    logger.addHandler(logging_handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    injector.binder.bind(logging.Logger, to=logger, scope=singleton)
    # Try setting locale
    try:
        locale.setlocale(locale.LC_ALL, "nb_NO.utf8")
    except:
        logger.warning("Missing locale nb_NO.utf8 on server")

    # Set up rabbitmq
    mq = AmqpConnection()
    mq.connect()
    mq.setup_exchange()
    mq.setup_queues()
    mq.setup_binding()
    def consume():
        mq.consume(on_message)
    consuming_thread = threading.Thread(target = consume)
    consuming_thread.start()

    # Set up scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_reply, trigger=IntervalTrigger(minutes=15))
    scheduler.add_job(invite_multiple_if_needed, trigger=IntervalTrigger(minutes=15))
    scheduler.add_job(send_reminders, trigger=IntervalTrigger(minutes=15))
    scheduler.add_job(sync_db_with_slack_and_return_count, trigger=IntervalTrigger(minutes=15))
    scheduler.start()

    # Set up slack app with socket mode
    handler = SocketModeHandler(app, slack_app_token)
    handler.start()

if __name__ == "__main__":
    main()