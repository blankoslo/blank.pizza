#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_bot_token)

def get_slack_users():
    return client.api_call(
        api_method="users.list"
    )['members']

def get_real_users(all_users):
    return [u for u in all_users if not u['deleted'] and not u['is_bot'] and not u['is_restricted'] and not u['name'] == "slackbot"] # type : list

def send_slack_message_old(channel_id, text, attachments=None, thread_ts=None):
    return client.api_call(
        api_method="chat.postMessage",
        params={
            "channel": channel_id,
            "as_user": True,
            "text": text,
            "attachments": attachments,
            "thread_ts": thread_ts
        }
    )

def send_slack_message(channel_id, text=None, blocks=None, thread_ts=None):
    return client.api_call(
        api_method="chat.postMessage",
        params={
            "channel": channel_id,
            "as_user": True,
            "blocks": blocks,
            "thread_ts": thread_ts,
            "text": text,
        }
    )

def update_slack_message(channel_id, ts, text=None, blocks=None):
    return client.api_call(
        api_method="chat.update",
        params={
            "channel": channel_id,
            "as_user": True,
            "text": text,
            "blocks": blocks,
            "ts": ts
        }
    )

def get_slack_message(channel_id, ts):
    try:
        # Call the conversations.history method using WebClient
        # conversations.history returns the first 100 messages by default
        # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination
        response = client.conversations_history(channel=channel_id, latest=ts, limit=1, inclusive=True)
        if response['ok'] and len(response['messages']) > 0:
            return response['messages'][0]
        return None
    except SlackApiError as e:
        return None
