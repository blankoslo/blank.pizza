#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import base64
import os
import time
import locale
import threading
import pytz

from src.api.bot_api import BotApi, BotApiConfiguration

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from injector import Injector, inject
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.broker.AmqpConnection import AmqpConnection

pizza_channel_id = os.environ["PIZZA_CHANNEL_ID"]
slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_app_token = os.environ["SLACK_APP_TOKEN"]

app = App(token=slack_bot_token)
injector = Injector()

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
    bot_api: BotApi = injector.get(BotApi)

    user = body["user"]
    user_id = user["id"]
    channel = body["channel"]
    channel_id = channel["id"]
    message = body["message"]
    invited_users = bot_api.get_invited_users()
    if user_id in invited_users:
        ts = message['ts']
        event_id = body["actions"][0]["value"]
        blocks = message["blocks"][0:3]
        if attending:
            bot_api.accept_invitation(event_id, user_id)
            bot_api.finalize_event_if_complete()
        else:
            bot_api.decline_invitation(event_id, user_id)
            bot_api.invite_multiple_if_needed()
        bot_api.send_pizza_invite_answered(channel_id, ts, event_id, blocks, attending)
    ack()

@app.action("rsvp_yes")
def handle_rsvp_yes(ack, body):
    handle_rsvp(body, ack, True)

@app.action("rsvp_no")
def handle_rsvp_no(ack, body):
    handle_rsvp(body, ack, False)

@app.action("rsvp_withdraw")
def handle_rsvp_withdraw(ack, body):
    bot_api: BotApi = injector.get(BotApi)

    message = body["message"]
    user = body["user"]
    user_id = user["id"]
    channel = body["channel"]
    channel_id = channel["id"]
    event_id = body["actions"][0]["value"]
    ts = message['ts']
    blocks = message["blocks"][0:3]
    failed_in_past = bot_api.withdraw_invitation(event_id, user_id)
    if not failed_in_past:
        bot_api.send_pizza_invite_withdraw(channel_id, ts, blocks)
        bot_api.invite_multiple_if_needed()
    else:
        bot_api.send_pizza_invite_withdraw_failure(channel_id, ts, blocks)
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
    bot_api: BotApi = injector.get(BotApi)

    channel = event["channel"]
    if 'files' in event:
        files = event['files']
        bot_api.send_slack_message_old(channel, u'Takk for fil! 🤙')
        headers = {u'Authorization': u'Bearer %s' % slack_bot_token}
        for file in files:
            r = requests.get(
                file['url_private'], headers=headers)
            b64 = base64.b64encode(r.content).decode('utf-8')
            payload = {'file': 'data:image;base64,%s' % b64,
                        'upload_preset': 'blank.pizza'}
            r2 = requests.post(
                'https://api.cloudinary.com/v1_1/blank/image/upload', data=payload)
            bot_api.save_image(
                r2.json()['public_id'], file['user'], file['title'])

# This only exists to make bolt not throw a warning that we dont handle the file_shared event
# We dont use this as we use the message event with subtype file_shared as that one
# contains a full file object with url_private, while this one only contains the ID
# Perhaps another file event contains the full object?
@app.event("file_shared")
def handle_file_shared_events(body, logger):
    logger.info(body)

def on_message(channel, method, properties, body):
    msg = body.decode('utf8')
    print(f'Time: {int(time.time()) % 1000} --- Message: {msg}')

def auto_reply():
    print("Auto replying on scheduled task")
    bot_api: BotApi = injector.get(BotApi)
    bot_api.auto_reply()

def invite_multiple_if_needed():
    print("Inviting multiple if need on scheduled task")
    bot_api: BotApi = injector.get(BotApi)
    bot_api.invite_multiple_if_needed()

def send_reminders():
    print("Sending reminders on scheduled task")
    bot_api: BotApi = injector.get(BotApi)
    bot_api.send_reminders()

def sync_db_with_slack_and_return_count():
    print("Syncing db with slack on scheduled task")
    bot_api: BotApi = injector.get(BotApi)
    bot_api.sync_db_with_slack_and_return_count()

def main():
    # Try setting locale
    try:
        locale.setlocale(locale.LC_ALL, "nb_NO.utf8")
    except:
        print("Missing locale nb_NO.utf8 on server")

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

    # Set up injector and bind rabbitmq
    injector.binder.bind(AmqpConnection, to=mq)
    api_config = BotApiConfiguration(pizza_channel_id, pytz.timezone('Europe/Oslo'))
    injector.binder.bind(BotApiConfiguration, to=api_config)

    # Set up scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_reply, trigger=IntervalTrigger(minutes=1))
    scheduler.add_job(invite_multiple_if_needed, trigger=IntervalTrigger(minutes=1))
    scheduler.add_job(send_reminders, trigger=IntervalTrigger(minutes=1))
    scheduler.add_job(sync_db_with_slack_and_return_count, trigger=IntervalTrigger(minutes=1))
    scheduler.start()

    # Set up slack app with socket mode
    handler = SocketModeHandler(app, slack_app_token)
    handler.start()

if __name__ == "__main__":
    main()
