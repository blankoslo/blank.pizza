from src.broker.handlers import MessageHandler
from src.broker.schemas.updated_invitation_event import UpdatedInvitationEventSchema
from src.api.bot_api import BotApi
from src.injector import injector
from src.rsvp import RSVP
from src.api.slack_api import SlackApi

@MessageHandler.handle('updated_invitation', UpdatedInvitationEventSchema)
def updated_invitation(invitation: dict):
    with injector.get(BotApi) as ba:
        if 'slack_message' in invitation:
            slack_client = SlackApi(token=invitation['bot_token'])

            event_id = invitation['event_id']
            slack_message_ts = invitation['slack_message']['ts']
            slack_message_channel_id = invitation['slack_message']['channel_id']

            if invitation['rsvp'] == RSVP.attending:
                ba.send_update_pizza_invite_attending(
                    channel_id=slack_message_channel_id,
                    ts=slack_message_ts,
                    event_id=event_id,
                    slack_client=slack_client
                )
            elif invitation['rsvp'] == RSVP.not_attending:
                ba.send_update_pizza_invite_not_attending(
                    channel_id=slack_message_channel_id,
                    ts=slack_message_ts,
                    event_id=event_id,
                    slack_client=slack_client
                )
            elif invitation['rsvp'] == RSVP.unanswered:
                ba.send_update_pizza_invite_unanswered(
                    channel_id=slack_message_channel_id,
                    ts=slack_message_ts,
                    event_id=event_id,
                    slack_client=slack_client
                )

