#!/usr/bin/env python
# -*- coding: utf-8 -*-

import src.api.slack as slack
import src.database.interface as db
import locale
import pytz
from datetime import datetime, timedelta
from src.database.rsvp import RSVP

try:
    locale.setlocale(locale.LC_ALL, "nb_NO.utf8")
except:
    print("Missing locale nb_NO.utf8 on server")

timezone = pytz.timezone('Europe/Oslo')

PEOPLE_PER_EVENT = 5
REPLY_DEADLINE_IN_HOURS = 24
DAYS_IN_ADVANCE_TO_INVITE = 10
HOURS_BETWEEN_REMINDERS = 4

def invite_if_needed():
    event = db.get_event_in_need_of_invitations(
        DAYS_IN_ADVANCE_TO_INVITE, PEOPLE_PER_EVENT)
    if event is None:
        print("No users were invited")
        return

    # timestamp (timestamp) is converted to UTC timestamp by psycopg2
    event_id, timestamp, restaurant_id, number_of_already_invited, restaurant_name = event
    # Convert timestamp to Norwegian timestamp
    timestamp = pytz.utc.localize(timestamp.replace(tzinfo=None), is_dst=None).astimezone(timezone)
    number_of_employees = sync_db_with_slack_and_return_count()
    number_to_invite = PEOPLE_PER_EVENT - number_of_already_invited
    users_to_invite = db.get_users_to_invite(number_to_invite, event_id, number_of_employees, PEOPLE_PER_EVENT)

    if len(users_to_invite) == 0:
        print("Event in need of users, but noone to invite") # TODO: needs to be handled
        return

    db.save_invitations(users_to_invite, event_id)

    for user_id in users_to_invite:
        send_pizza_invite(user_id, event_id, restaurant_name, timestamp.strftime("%A %d. %B kl %H:%M"), REPLY_DEADLINE_IN_HOURS)
        print("%s was invited to event on %s" % (user_id, timestamp))

def send_reminders():
    inviations = db.get_unanswered_invitations()

    for invitation in inviations:
        # invited_at and reminded_at (timestamps) are converted to UTC timestamp by psycopg2
        slack_id, invited_at, reminded_at = invitation
        # all timestamps (such as reminded_at) gets converted to UTC
        # so comparing it to datetime.now in UTC is correct
        remind_timestamp = datetime.now(pytz.utc) + timedelta(hours=-HOURS_BETWEEN_REMINDERS)
        if(reminded_at < remind_timestamp):
            slack.send_slack_message(slack_id, "Hei du! Jeg hørte ikke noe mer? Er du gira? (ja/nei)")
            db.update_reminded_at(slack_id)
            print("%s was reminded about an event." % slack_id)

def finalize_event_if_complete():
    event = db.get_event_ready_to_finalize(PEOPLE_PER_EVENT)
    if event is None:
        print("No events ready to finalize")
    else:
        # timestamp (timestamp) is converted to UTC timestamp by psycopg2
        event_id, timestamp, place = event
        # Convert timestamp to Norwegian timestamp
        timestamp = pytz.utc.localize(timestamp.replace(tzinfo=None), is_dst=None).astimezone(timezone)
        sync_db_with_slack_and_return_count()
        slack_ids = ['<@%s>' % user for user in db.get_attending_users(event_id)]
        db.mark_event_as_finalized(event_id)
        ids_string = ", ".join(slack_ids)
        # TODO change this from using pizza name as id to actual id
        slack.send_slack_message('#pizza', "Halloi! %s! Dere skal spise 🍕 på %s, %s. %s booker bord, og %s legger ut for maten. Blank betaler!" % (ids_string, place, timestamp.strftime("%A %d. %B kl %H:%M"), slack_ids[0], slack_ids[1]))

def auto_reply():
    users_that_did_not_reply = db.auto_reply_after_deadline(REPLY_DEADLINE_IN_HOURS)
    if users_that_did_not_reply is None:
       return

    for user_id in users_that_did_not_reply:
        slack.send_slack_message(user_id, "Neivel, da antar jeg du ikke kan/gidder. Håper du blir med neste gang! 🤞")
        print("%s didn't answer. Setting RSVP to not attending.")

def save_image(cloudinary_id, slack_id, title):
    db.save_image(cloudinary_id, slack_id, title)

def rsvp(slack_id, answer):
    db.rsvp(slack_id, answer)


def send_slack_message_old(channel_id, text, attachments=None, thread_ts=None):
    return slack.send_slack_message_old(channel_id, text, attachments, thread_ts)

def update_slack_message(channel_id, ts, text=None, blocks=None):
    return slack.update_slack_message(channel_id, ts, text, blocks)

def send_pizza_invite(channel_id, event_id, place, datetime, deadline):
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
    return slack.send_slack_message(channel_id=channel_id, blocks=blocks)

def send_pizza_invite_answered(channel_id, ts, event_id, old_blocks, attending):
    for block in old_blocks:
        del block["block_id"]
        if ("text" in block and "emoji" in block["text"]):
            del block["text"]["emoji"]
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
				"value": event_id,
				"action_id": "rsvp_withdraw"
			}
		}
    ]
    blocks = old_blocks + new_blocks_common
    if attending:
        blocks += new_blocks_yes
    return slack.update_slack_message(channel_id=channel_id, ts=ts, blocks=blocks)

def get_invited_users():
    return db.get_invited_users()

def sync_db_with_slack_and_return_count():
  slack_users = slack.get_real_users(slack.get_slack_users())
  db.update_slack_users(slack_users)
  return len(slack_users)
