#!/usr/bin/env python
# -*- coding: utf-8 -*-

import api

from slackclient import SlackClient
from time import sleep

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)

if sc.rtm_connect():
    while True:
        event_list = sc.rtm_read()
        for event in event_list:
            print 'Event :', event

        message_list = list(filter(lambda m: m['type'] == 'message', event_list))
        for message in message_list:
            if 'file' in message:
                api.send_slack_message(message['channel'], u'Takk for fil! 🤙')
            else:
                print message['user']
                print api.get_invited_users()
                if message['user'] in api.get_invited_users():
                    if message['text'].lower() == 'ja':
                        api.rsvp(message['user'], 'attending')
                        api.send_slack_message(message['channel'], u'Sweet! 🤙')
                        api.finalize_event_if_complete()
                    elif message['text'].lower() == 'nei':
                        api.rsvp(message['user'], 'not attending')
                        api.send_slack_message(message['channel'], u'Ok 😏')
                        api.invite_if_needed()
                    else:
                        api.send_slack_message(message['channel'], u'Hehe jeg er litt dum, jeg. Skjønner jeg ikke helt hva du mener 😳. Kan du være med? (ja/nei)')
        sleep(0.5)

else:
    print "Connection Failed, invalid token?"
