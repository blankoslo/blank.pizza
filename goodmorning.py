#!/usr/bin/env python
# -*- coding: utf-8 -*-

import api
import floq_db
import db

channel = '#random'


def create_mention_string(slack_ids_map):
    slack_ids = list(slack_ids_map)
    if len(slack_ids) < 1:
        raise ValueError('Noone to mention!')
    elif len(slack_ids) == 1:
        return slack_ids[0]
    elif len(slack_ids) == 2:
        return '%s og %s' % (slack_ids[0], slack_ids[1])
    elif len(slack_ids) > 2:
        mention_string = ", ".join(slack_ids[:-1])
        return mention_string + " og %s" % slack_ids[-1]


def mention_people(people, message):
    slack_ids = db.get_slack_ids_from_emails(people)

    if len(slack_ids) > 0:
        mention_ids = map(lambda x: '<@%s>' % x, slack_ids)
        mention_string = create_mention_string(mention_ids)
        return api.send_slack_message(
            channel, message % mention_string)


api.sync_db_with_slack_and_return_count()

first_day_resp = mention_people(floq_db.get_users_with_first_day(),
                                "I dag har %s sin første dag i Blank!")
api.send_slack_message(channel, "Velkommen 🌹", thread_ts=first_day_resp['ts'])

birthday_resp = mention_people(floq_db.get_users_with_birthday(),
                               "I dag har %s bursdag!")
api.send_slack_message(channel, "Gratulerer 🎈", thread_ts=birthday_resp['ts'])
