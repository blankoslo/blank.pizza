#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackApi:
    def __init__(self, client=None, token=None):
        if client is not None:
            self.client = client
        elif token is not None:
            self.client = WebClient(token=token)
        else:
            raise ValueError("Either 'client' or 'token' must be provided.")

    def get_slack_users(self):
        return self.client.api_call(
            api_method="users.list"
        )['members']

    def get_real_users(self, all_users):
        return [u for u in all_users if not u['deleted'] and not u['is_bot'] and not u['is_restricted'] and not u['name'] == "slackbot"] # type : list

    def send_slack_message_old(self, channel_id, text, attachments=None, thread_ts=None):
        return self.client.api_call(
            api_method="chat.postMessage",
            params={
                "channel": channel_id,
                "as_user": True,
                "text": text,
                "attachments": attachments,
                "thread_ts": thread_ts
            }
        )

    def send_slack_message(self, channel_id, text=None, blocks=None, thread_ts=None):
        return self.client.api_call(
            api_method="chat.postMessage",
            params={
                "channel": channel_id,
                "as_user": True,
                "blocks": blocks,
                "thread_ts": thread_ts,
                "text": text,
            }
        )

    def update_slack_message(self, channel_id, ts, text=None, blocks=None):
        return self.client.api_call(
            api_method="chat.update",
            params={
                "channel": channel_id,
                "as_user": True,
                "text": text,
                "blocks": blocks,
                "ts": ts
            }
        )

    def get_slack_message(self, channel_id, ts):
        try:
            # Call the conversations.history method using WebClient
            # conversations.history returns the first 100 messages by default
            # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination
            response = self.client.conversations_history(channel=channel_id, latest=ts, limit=1, inclusive=True)
            if response['ok'] and len(response['messages']) > 0:
                return response['messages'][0]
            return None
        except SlackApiError as e:
            return None
