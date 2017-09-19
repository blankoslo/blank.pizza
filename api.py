#!/usr/bin/env python
# -*- coding: utf-8 -*-

import slack
import db
import locale
from datetime import datetime, timedelta

locale.setlocale(locale.LC_ALL, "no_NO")

PEOPLE_PER_EVENT = 5
REPLY_DEADLINE_IN_HOURS = 24
DAYS_IN_ADVANCE_TO_INVITE = 9
HOURS_BETWEEN_REMINDERS = 4

def invite_if_needed():
    event = db.get_event_in_need_of_invitations(DAYS_IN_ADVANCE_TO_INVITE, PEOPLE_PER_EVENT)
    if event is None:
        print("No users were invited")
        return

    event_id, timestamp, place, number_of_already_invited = event
    number_of_employees = sync_db_with_slack_and_return_count()
    number_to_invite = PEOPLE_PER_EVENT - number_of_already_invited
    users_to_invite = db.get_users_to_invite(number_to_invite, event_id, number_of_employees, PEOPLE_PER_EVENT)

    if len(users_to_invite) == 0:
        print("Event in need of users, but noone to invite") # TODO: needs to be handled
        return

    db.save_invitations(users_to_invite, event_id)

    for user_id in users_to_invite:
        slack.send_slack_message(user_id, "Du er invitert til 🍕 på %s, %s. Pls svar innen %d timer 🙏. Kan du? (ja/nei)" % (place, timestamp.strftime("%A %d. %B kl %H:%M"), REPLY_DEADLINE_IN_HOURS))
        print("%s was invited to event on %s" % (user_id, timestamp))

def send_reminders():
    inviations = db.get_unanswered_invitations()

    for invitation in inviations:
        slack_id, invited_at, reminded_at = invitation
        remind_timestamp = datetime.now() + timedelta(hours=-HOURS_BETWEEN_REMINDERS)
        if(reminded_at < remind_timestamp):
            slack.send_slack_message(slack_id, "Hei du! Jeg hørte ikke noe mer? Er du gira? (ja/nei)")
            db.update_reminded_at(slack_id)
            print("%s was reminded about an event." % slack_id)

def finalize_event_if_complete():
    event = db.get_event_ready_to_finalize(PEOPLE_PER_EVENT)
    if event is None:
        print("No events ready to finalize")
    else:
        event_id, timestamp, place = event
        sync_db_with_slack_and_return_count()
        slack_ids = ['<@%s>' % user for user in db.get_attending_users(event_id)]
        db.mark_event_as_finalized(event_id)
        ids_string = ", ".join(slack_ids)
        slack.send_slack_message('#pizza', "Halloi! %s! Dere skal spise 🍕 på %s, %s. Blank betaler!" % (ids_string, place, timestamp))


def auto_reply():
    users_that_did_not_reply = db.auto_reply_after_deadline(REPLY_DEADLINE_IN_HOURS)

    for user_id in users_that_did_not_reply:
        slack.send_slack_message(user_id, "Neivel, da antar jeg du ikke er interessert. Håper du blir med neste gang!")
        print("%s didn't answer. Setting RSVP to not attending.")

def save_image(cloudinary_id, slack_id, title):
    db.save_image(cloudinary_id, slack_id, title)

def rsvp(slack_id, answer):
    db.rsvp(slack_id, answer)

def send_slack_message(channel_id, text):
    slack.send_slack_message(channel_id, text)

def get_invited_users():
    return db.get_invited_users()

def sync_db_with_slack_and_return_count():
  slack_users = slack.get_real_users(slack.get_slack_users())
  db.update_slack_users(slack_users)
  return len(slack_users)
