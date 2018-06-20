#!/usr/bin/env python
# -*- coding: utf-8 -*-

import api
import floq_db
import db


def create_mention_string(slack_ids):
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
        api.send_slack_message(
            '#test', message % mention_string)


api.sync_db_with_slack_and_return_count()

mention_people(floq_db.get_users_with_first_day(),
               "I dag har %s sin første dag i Blank! Velkommen 🌹")

mention_people(floq_db.get_users_with_birthday(),
               "I dag har %s bursdag! Gratulerer 🎈")
