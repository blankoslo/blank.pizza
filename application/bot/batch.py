#!/usr/bin/env python
# -*- coding: utf-8 -*-

import src.api.bot_api as api

api.auto_reply()
api.invite_multiple_if_needed()
api.send_reminders()
