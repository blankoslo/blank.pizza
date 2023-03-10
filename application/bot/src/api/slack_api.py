import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from src.injector import injector


class SlackApi:
    def __init__(self, client=None, token=None):
        if client is not None:
            self.client = client
        elif token is not None:
            self.client = WebClient(token=token)
        else:
            raise ValueError("Either 'client' or 'token' must be provided.")
        self.logger = injector.get(logging.Logger)

    def get_slack_users(self):
        first_page = self.client.users_list()

        if not first_page["ok"]:
            self.logger(first_page["error"])
            return []

        members = first_page["members"]

        # Continue to loop over pages to find the default channel
        next_cursor = first_page["response_metadata"]["next_cursor"]
        while next_cursor != "":
            page = self.client.conversations_list(cursor=next_cursor)
            next_cursor = page["response_metadata"]["next_cursor"]

            members = members.extend(page["members"])

        return members

    def get_real_users(self, all_users):
        return [u for u in all_users if not u['deleted'] and not u['is_bot'] and not u['is_restricted'] and not u['name'] == "slackbot"] # type : list

    def send_slack_message(self, channel_id, text=None, blocks=None, thread_ts=None):
        return self.client.chat_postMessage(
            channel=channel_id,
            as_user=True,
            blocks=blocks,
            thread_ts=thread_ts,
            text=text
        )

    def update_slack_message(self, channel_id, ts, text=None, blocks=None):
        return self.client.chat_update(
            channel=channel_id,
            as_user=True,
            text=text,
            blocks=blocks,
            ts=ts
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
            self.logger.error(e)
            return None

    def get_default_channel(self):
        first_page = self.client.conversations_list()

        # If response is not OK then we return None as we didnt find a channel
        if not first_page["ok"]:
            self.logger(first_page["error"])
            return None

        # Try to find default channel in first page
        for channel in first_page['channels']:
            if channel["is_general"]:
                return channel

        # Continue to loop over pages to find the default channel
        next_cursor = first_page["response_metadata"]["next_cursor"]
        while next_cursor != "":
            page = self.client.conversations_list(cursor=next_cursor)
            next_cursor = page["response_metadata"]["next_cursor"]

            for channel in page['channels']:
                if channel["is_general"]:
                    return channel

        # If all else failed then return None as we didnt find it
        self.logger.warn("Was unable to find default channel")
        return None

    def get_channel_info(self, channel_id):
        try:
            res = self.client.conversations_info(channel=channel_id)
            if not res["ok"]:
                raise Exception(res["error"])
            return res["channel"]
        except:
            return None

    def join_channel(self, channel_id):
        try:
            channel = self.get_channel_info(channel_id=channel_id)
            if channel["is_member"]:
                return True

            res = self.client.conversations_join(channel=channel_id)
            if not res["ok"]:
                raise Exception(res["error"])

            return True
        except:
            return False

    def leave_channel(self, channel_id):
        try:
            res = self.client.conversations_leave(channel=channel_id)
            if not res["ok"]:
                raise Exception(res["error"])
        except:
            return False
        return True
