#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytz
import os
from injector import inject

from src.api.slack_api import SlackApi
from datetime import datetime, timedelta
from src.rsvp import RSVP
from src.broker.broker_client import BrokerClient
from src.injector import injector
import logging

class BotApiConfiguration:
    def __init__(self, pizza_channel_id, timezone):
        self.pizza_channel_id = pizza_channel_id
        self.timezone = timezone

class BotApi:
    @inject
    def __init__(self, config: BotApiConfiguration, logger: logging.Logger):
        self.REPLY_DEADLINE_IN_HOURS = int(os.environ["REPLY_DEADLINE_IN_HOURS"])
        self.HOURS_BETWEEN_REMINDERS = int(os.environ["HOURS_BETWEEN_REMINDERS"])
        self.pizza_channel_id = config.pizza_channel_id
        self.timezone = config.timezone
        self.logger = logger

    def __enter__(self):
        self.client = injector.get(BrokerClient)
        return self

    def __exit__(self, type, value, traceback):
        self.client.disconnect()

    def invite_multiple_if_needed(self):
        events = self.client.invite_multiple_if_needed()
        for event in events:
            slack_client = SlackApi(token=event["bot_token"])
            self.invite_if_needed(event, slack_client)

    def invite_if_needed(self, event, slack_client):
        self.logger.info("Inviting users for %s", event['event_id'])
        invited_users = event['invited_users']
        event_time = event['event_time']
        event_id = event['event_id']
        restaurant_name = event['restaurant_name']

        # timestamp (timestamp) is converted to UTC timestamp by psycopg2
        # Convert timestamp to Norwegian timestamp
        timestamp = pytz.utc.localize(event_time.replace(tzinfo=None), is_dst=None).astimezone(self.timezone)

        for user_id in invited_users:
            slack_message = self.send_pizza_invite(user_id, str(event_id), restaurant_name, timestamp.strftime("%A %d. %B kl %H:%M"), self.REPLY_DEADLINE_IN_HOURS, slack_client = slack_client)
            if not slack_message['ok']:
                self.logger.warn("Failed to send invitation to %s", user_id)
                continue
            self.logger.info("%s was invited to event on %s" % (user_id, timestamp))
            self.client.update_invitation(
                user_id,
                event_id,
                {
                    'slack_message': {
                        'ts': slack_message['ts'],
                        'channel_id': slack_message['channel']
                    }
                }
            )

    def send_reminders(self):
        invitations = self.client.get_unanswered_invitations()

        for invitation in invitations:
            slack_client = SlackApi(token = "TODO")
            # all timestamps (such as reminded_at) gets converted to UTC
            # so comparing it to datetime.now in UTC is correct
            remind_timestamp = datetime.now(pytz.utc) + timedelta(hours =- self.HOURS_BETWEEN_REMINDERS)
            if invitation['reminded_at'] < remind_timestamp:
                slack_client.send_slack_message(invitation['slack_id'], "Hei du! Jeg hørte ikke noe mer? Er du gira?")
                was_updated = self.client.update_invitation(
                    slack_id = invitation['slack_id'],
                    event_id = invitation['event_id'],
                    update_values = {
                        "reminded_at": datetime.now().isoformat()
                    }
                )
                if was_updated:
                    self.logger.info("%s was reminded about an event." % invitation['slack_id'])
                else:
                    self.logger.warning("failed to update invitation")

    def send_event_finalized(self, timestamp, restaurant_name, slack_ids):
        slack_client = SlackApi(token = "TODO")
        self.logger.info("Finalizing event %s %s", timestamp, restaurant_name)
        # Convert timestamp to Norwegian timestamp
        timestamp = pytz.utc.localize(timestamp.replace(tzinfo=None), is_dst=None).astimezone(self.timezone)
        # Create slack @-id-strings
        users = ['<@%s>' % user for user in slack_ids]
        ids_string = ", ".join(users)
        # Get the user to book
        booker = users[0]
        # Get the user to pay
        payer = users[1] if len(users) > 1 else users[0]
        # Send the finalization Slack message
        slack_client.send_slack_message(self.pizza_channel_id, "Halloi! %s! Dere skal spise 🍕 på %s, %s. %s booker bord, og %s legger ut for maten. Blank betaler!" % (ids_string, restaurant_name, timestamp.strftime("%A %d. %B kl %H:%M"), booker, payer))

    def send_event_unfinalized(self, timestamp, restaurant_name, slack_ids):
        slack_client = SlackApi(token = "TODO")
        self.logger.info("Unfinalizing event %s %s", timestamp, restaurant_name)
        # Convert timestamp to Norwegian timestamp
        timestamp = pytz.utc.localize(timestamp.replace(tzinfo=None), is_dst=None).astimezone(self.timezone)
        # Create slack @-id-strings
        users = ['<@%s>' % user for user in slack_ids]
        ids_string = ", ".join(users)
        # Send message that the event unfinalized
        slack_client.send_slack_message(self.pizza_channel_id, "Halloi! %s! Hvis den som meldte seg av besøket til  %s  %s skulle betale eller booke så må nesten en av dere andre sørge for det. I mellomtiden letes det etter en erstatter." % (ids_string, restaurant_name, timestamp.strftime("%A %d. %B kl %H:%M")))
        # Invite more users for the event
        self.invite_multiple_if_needed()

    def send_user_withdrew_after_finalization(self, user_id, timestamp, restaurant_name):
        slack_client = SlackApi(token = "TODO")
        self.logger.info("User %s withdrew from event %s %s", user_id, timestamp, restaurant_name)
        # Send message that the user withdrew
        slack_client.send_slack_message(self.pizza_channel_id, "Halloi! <@%s> meldte seg nettopp av besøket til %s %s." % (user_id, restaurant_name, timestamp.strftime("%A %d. %B kl %H:%M")))
        # Invite more users for the event
        self.invite_multiple_if_needed()

    def auto_reply(self):
        invitations = self.client.get_unanswered_invitations()

        for invitation in invitations:
            slack_client = SlackApi(token = "TODO")
            deadline = invitation['invited_at'] + timedelta(hours=self.REPLY_DEADLINE_IN_HOURS)
            if deadline < datetime.now(pytz.utc):
                was_updated = self.update_invitation_answer(
                    slack_id = invitation['slack_id'],
                    event_id = invitation['event_id'],
                    answer = RSVP.not_attending
                )
                if was_updated:
                    # Update invitation message - remove buttons and tell user it expired
                    if 'slack_message' in invitation:
                        channel_id = invitation['slack_message']['channel_id']
                        ts = invitation['slack_message']['ts']
                        invitation_message = slack_client.get_slack_message(channel_id, ts)
                        blocks = invitation_message["blocks"][0:3]
                        self.send_invitation_expired(channel_id, ts, blocks, slack_client = slack_client)
                    # Send the user a message that the invite expired
                    slack_client.send_slack_message(invitation['slack_id'], "Neivel, da antar jeg du ikke kan/gidder. Håper du blir med neste gang! 🤞")
                    self.logger.info("%s didn't answer. Setting RSVP to not attending." % invitation['slack_id'])
                else:
                    self.logger.warning("failed to update invitation to not attending")

    def clean_up_invitations(self):
        invitations = self.client.get_unanswered_invitations_on_finished_events_and_set_not_attending()

        for invitation in invitations:
            slack_client = SlackApi(token = "TODO")
            # Update invitation message - remove buttons and tell user it expired
            if not 'invitation' in invitation:
                continue
            channel_id = invitation['slack_message']['channel_id']
            ts = invitation['slack_message']['ts']
            invitation_message = slack_client.get_slack_message(channel_id, ts)
            blocks = invitation_message["blocks"][0:3]
            self.send_invitation_expired(channel_id, ts, blocks, slack_client = slack_client)
            self.logger.info("%s didn't answer and event is finished. Removing accept/decline buttons" % invitation['slack_id'])

    def update_invitation_answer(self, slack_id, event_id, answer: RSVP):
        return self.client.update_invitation(
            slack_id = slack_id,
            event_id = event_id,
            update_values = {
                "rsvp": answer
            }
        )

    def accept_invitation(self, event_id, slack_id):
        self.update_invitation_answer(slack_id = slack_id, event_id = event_id, answer = RSVP.attending)

    def decline_invitation(self, event_id, slack_id):
        self.update_invitation_answer(slack_id = slack_id, event_id = event_id, answer = RSVP.not_attending)

    def withdraw_invitation(self, event_id, slack_id):
        return self.client.withdraw_invitation(event_id = event_id, slack_id = slack_id)

    def save_image(self, cloudinary_id, slack_id, title):
        self.client.create_image(cloudinary_id = cloudinary_id, slack_id = slack_id, title = title)

    def get_invited_users(self):
        return self.client.get_invited_unanswered_user_ids()

    def sync_db_with_slack(self):
        slack_organizations = self.client.get_slack_organizations()
        for slack_organization in slack_organizations:
            slack_client = SlackApi(token=slack_organization['bot_token'])
            all_slack_users = slack_client.get_slack_users()
            slack_users = slack_client.get_real_users(all_slack_users)
            response = self.client.update_slack_user(slack_users)

            updated_users = response['updated_users']
            for user in updated_users:
                self.logger.info("Updated user %s" % user)
            failed_users = response['failed_users']
            for user in failed_users:
                self.logger.warning("Was unable to update %s" % user)

    def inform_users_unfinalized_event_got_cancelled(self, time, restaurant_name, slack_data):
        self.logger.info("unfinalized event got cancelled")
        slack_client = SlackApi(token = "TODO")
        for slack_user_data in slack_data:
            slack_id = slack_user_data['user_id']
            # Update invitation message - remove buttons and tell user it has been cancelled
            channel_id = slack_user_data['invitation_message']['channel_id']
            ts = slack_user_data['invitation_message']['ts']
            invitation_message = slack_client.get_slack_message(channel_id, ts)
            blocks = invitation_message["blocks"][0:3]
            self.send_invitation_invalidated_event_cancelled(channel_id, ts, blocks, slack_client = slack_client)
            # Send the user a message that the event has been cancelled
            slack_client.send_slack_message(slack_id, "Halloi! Besøket til %s, %s har blitt kansellert. Sorry!" % (restaurant_name, time.strftime("%A %d. %B kl %H:%M")))
            self.logger.info("Informed user: %s" % slack_id)

    def inform_users_finalized_event_got_cancelled(self, time, restaurant_name, slack_data):
        slack_client = SlackApi(token = "TODO")
        # Send the users a message in the pizza channel that the event has been cancelled
        slack_user_ids = [user['user_id'] for user in slack_data]
        users = ['<@%s>' % user_id for user_id in slack_user_ids]
        ids_string = ", ".join(users)
        self.logger.info("finalized event got cancelled for users %s" % ", ".join(slack_user_ids))
        slack_client.send_slack_message(self.pizza_channel_id, "Halloi! %s! Besøket til %s, %s har blitt kansellert. Sorry!" % (ids_string, restaurant_name, time.strftime("%A %d. %B kl %H:%M"),))
        # Update invitation message - remove buttons and tell user it has been cancelled
        for slack_user_data in slack_data:
            channel_id = slack_user_data['invitation_message']['channel_id']
            ts = slack_user_data['invitation_message']['ts']
            invitation_message = slack_client.get_slack_message(channel_id, ts)
            blocks = invitation_message["blocks"][0:3]
            self.send_invitation_invalidated_event_cancelled(channel_id, ts, blocks, slack_client = slack_client)

    def inform_users_unfinalized_event_got_updated(self, old_time, time, old_restaurant_name, restaurant_name, slack_ids):
        self.logger.info("unfinalized event got updated")
        slack_client = SlackApi(token = "TODO")
        for slack_id in slack_ids:
            slack_client.send_slack_message(slack_id, "Halloi! Besøket til %s, %s har blit endret til %s, %s." % (old_restaurant_name, old_time.strftime("%A %d. %B kl %H:%M"), restaurant_name, time.strftime("%A %d. %B kl %H:%M")))
            self.logger.info("Informed user: %s" % slack_id)

    def inform_users_finalized_event_got_updated(self, old_time, time, old_restaurant_name, restaurant_name, slack_ids):
        slack_client = SlackApi(token = "TODO")
        users = ['<@%s>' % user for user in slack_ids]
        ids_string = ", ".join(users)
        self.logger.info("finalized event got updated for users %s" % ", ".join(slack_ids))
        slack_client.send_slack_message(self.pizza_channel_id, "Halloi! %s! Besøket til %s, %s har blit endret til %s, %s." % (ids_string, old_restaurant_name, old_time.strftime("%A %d. %B kl %H:%M"), restaurant_name, time.strftime("%A %d. %B kl %H:%M")))

    def send_slack_message_old(self, channel_id, text, slack_client, attachments=None, thread_ts=None):
        return slack_client.send_slack_message_old(channel_id, text, attachments, thread_ts)

    def update_slack_message(self, channel_id, ts, slack_client, text=None, blocks=None):
        return slack_client.update_slack_message(channel_id, ts, text, blocks)

    def send_pizza_invite(self, channel_id, event_id, place, datetime, deadline, slack_client):
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Pizzainvitasjon"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"Du er invitert til :pizza: på {place}, {datetime}. Pls svar innen {deadline} timer :pray:. Kan du?"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Hells yesss!!! 🍕🍕🍕"
                        },
                        "value": event_id,
                        "action_id": "rsvp_yes",
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Nah ☹️"
                        },
                        "value": event_id,
                        "action_id": "rsvp_no",
                    }
                ]
            }
        ]
        return slack_client.send_slack_message(channel_id=channel_id, blocks=blocks)

    def clean_blocks(self, blocks):
        for block in blocks:
            del block["block_id"]
            if "text" in block and "emoji" in block["text"]:
                del block["text"]["emoji"]
        return blocks

    def send_update_pizza_invite_attending(self, channel_id, ts, event_id, slack_client):
        self.logger.info('updating invitation message to attending for %s, %s' % (channel_id, event_id))
        invitation_message = slack_client.get_slack_message(channel_id, ts)
        blocks = invitation_message["blocks"][0:3]
        message = self.send_pizza_invite_answered(
            channel_id=channel_id,
            ts=ts,
            event_id=event_id,
            old_blocks=blocks,
            attending=True,
            slack_client = slack_client
        )
        self.logger.info(message)

    def send_update_pizza_invite_not_attending(self, channel_id, ts, event_id, slack_client):
        self.logger.info('updating invitation message to not_attending for %s, %s' % (channel_id, event_id))
        invitation_message = slack_client.get_slack_message(channel_id, ts)
        blocks = invitation_message["blocks"][0:3]
        self.send_pizza_invite_answered(
            channel_id=channel_id,
            ts=ts,
            event_id=event_id,
            old_blocks=blocks,
            attending=False,
            slack_client = slack_client
        )

    def send_update_pizza_invite_unanswered(self, channel_id, ts, event_id, slack_client):
        self.logger.info('updating invitation message to unanswered for %s, %s' % (channel_id, event_id))
        invitation_message = slack_client.get_slack_message(channel_id, ts)
        blocks = invitation_message["blocks"][0:3]
        old_blocks = self.clean_blocks(blocks)
        new_blocks = [{
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Hells yesss!!! 🍕🍕🍕"
                    },
                    "value": str(event_id),
                    "action_id": "rsvp_yes",
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Nah ☹️"
                    },
                    "value": str(event_id),
                    "action_id": "rsvp_no",
                }
            ]
        }]
        blocks = old_blocks + new_blocks
        return slack_client.update_slack_message(channel_id=channel_id, ts=ts, blocks=blocks)

    def send_pizza_invite_answered(self, channel_id, ts, event_id, old_blocks, attending, slack_client):
        old_blocks = self.clean_blocks(old_blocks)
        new_blocks_common = [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"Du har takket {'ja. Sweet! 🤙' if attending else 'nei. Ok 😕'}",
                }
            }
        ]
        new_blocks_yes = [
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hvis noe skulle skje så kan du melde deg av ved å klikke på knappen!"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Meld meg av"
                    },
                    "value": str(event_id),
                    "action_id": "rsvp_withdraw"
                }
            }
        ]
        blocks = old_blocks + new_blocks_common
        if attending:
            blocks += new_blocks_yes
        return slack_client.update_slack_message(channel_id=channel_id, ts=ts, blocks=blocks)

    def send_invitation_invalidated_event_cancelled(self, channel_id, ts, old_blocks, slack_client):
        old_blocks = self.clean_blocks(old_blocks)
        new_blocks = [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "Arrangementet har blitt avlyst.",
                }
            }
        ]
        blocks = old_blocks + new_blocks
        return slack_client.update_slack_message(channel_id=channel_id, ts=ts, blocks=blocks)

    def send_invitation_expired(self, channel_id, ts, old_blocks, slack_client):
        old_blocks = self.clean_blocks(old_blocks)
        new_blocks = [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "Invitasjonen er utløpt.",
                }
            }
        ]
        blocks = old_blocks + new_blocks
        return slack_client.update_slack_message(channel_id=channel_id, ts=ts, blocks=blocks)

    def send_pizza_invite_withdraw(self, channel_id, ts, old_blocks, slack_client):
        old_blocks = self.clean_blocks(old_blocks)
        new_blocks = [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "Du har meldt deg av. Ok 😕",
                }
            }
        ]
        blocks = old_blocks + new_blocks
        return slack_client.update_slack_message(channel_id=channel_id, ts=ts, blocks=blocks)

    def send_pizza_invite_withdraw_failure(self, channel_id, ts, old_blocks, slack_client):
        old_blocks = self.clean_blocks(old_blocks)
        new_blocks = [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "Pizza arrangementet er over. Avmelding er ikke mulig.",
                }
            }
        ]
        blocks = old_blocks + new_blocks
        return slack_client.update_slack_message(channel_id=channel_id, ts=ts, blocks=blocks)
