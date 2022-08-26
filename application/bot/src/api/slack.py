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

def send_slack_message(channel_id, text, attachments=None, thread_ts=None):
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
