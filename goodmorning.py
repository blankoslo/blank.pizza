#!/usr/bin/env python
# -*- coding: utf-8 -*-

import api
import floq_db

users_with_first_day = floq_db.get_users_with_first_day()

for user in users_with_first_day:
    first_name = user
    api.send_slack_message(
        '#general', "Idag har %s sin første dag i Blank! Velkommen 🌹" % first_name)
