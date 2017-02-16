from slackclient import SlackClient
from time import sleep

slack_token = os.environ["SLACK_API_TOKEN"] # type: str
sc = SlackClient(slack_token)

if sc.rtm_connect():
    while True:
        event_list = sc.rtm_read() # type: list
        for event in event_list:
            print 'Event :', event

        message_list = list(filter(lambda m: m['type'] == 'message', event_list)) # type: list
        for message in message_list:
            if 'file' in message    :
                print 'File :', message['file']['url_private_download']
            else:
                print 'Message :', message['text'], ' from ', message['user']
        sleep(1)

else:
    print "Connection Failed, invalid token?"
