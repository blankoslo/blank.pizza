#!/usr/bin/env python
# -*- coding: utf-8 -*-

import api
import os
import requests
import base64

from slackclient import SlackClient
from time import sleep

pizza_channel_id = 'C2NC8DBN1'

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)


def is_dm(message):
    return message['channel'][0] == 'D'


if sc.rtm_connect():
    while True:
        event_list = sc.rtm_read()
        message_list = list(
            filter(lambda m: m['type'] == 'message', event_list))
        for message in message_list:
            if(message['channel'] == pizza_channel_id):
                if 'files' in message:
                    api.send_slack_message(
                        message['channel'], u'Takk for fil! 🤙')
                    headers = {u'Authorization': u'Bearer %s' % slack_token}
                    for file in message['files']:
                        r = requests.get(
                            file['url_private'], headers=headers)
                        b64 = base64.b64encode(r.content).decode('utf-8')
                        payload = {'file': 'data:image;base64,%s' % b64,
                                   'upload_preset': 'blank.pizza'}
                        r2 = requests.post(
                            'https://api.cloudinary.com/v1_1/blank/image/upload', data=payload)
                        api.save_image(
                            r2.json()['public_id'], file['user'], file['title'])
            elif(is_dm(message)):
                if message['user'] in api.get_invited_users():
                    if message['text'].lower() == 'ja':
                        api.rsvp(message['user'], 'attending')
                        api.send_slack_message(
                            message['channel'], u'Sweet! 🤙')
                        api.finalize_event_if_complete()
                    elif message['text'].lower() == 'nei':
                        api.rsvp(message['user'], 'not attending')
                        api.send_slack_message(message['channel'], u'Ok 😏')
                        api.invite_if_needed()
                    else:
                        api.send_slack_message(
                            message['channel'], u'Hehe jeg er litt dum, jeg. Skjønner jeg ikke helt hva du mener 😳. Kan du være med? (ja/nei)')
        sleep(0.5)

else:
    print("Connection Failed, invalid token?")
