from datetime import datetime
import pytz
import os

from app.services.broker import BrokerService
from app.services.broker.handlers.message_handler import MessageHandler

from app.services.broker.schemas.withdraw_invitation import WithdrawInvitationRequestSchema, WithdrawInvitationResponseSchema
from app.services.broker.schemas.invite_multiple_if_needed import InviteMultipleIfNeededResponseSchema

from app.models.event import Event
from app.models.user import User
from app.models.slack_user import SlackUser
from app.models.invitation import Invitation
from app.models.invitation_schema import InvitationSchema
from app.models.enums import RSVP
from app.services.injector import injector
from app.services.invitation_service import InvitationService

@MessageHandler.handle('withdraw_invitation')
def withdraw_invitation(payload: dict, correlation_id: str, reply_to: str):
    invitation_service = injector.get(InvitationService)

    schema = WithdrawInvitationRequestSchema()
    request = schema.load(payload)
    event_id = request.get('event_id')
    slack_id = request.get('slack_id')

    try:
        updated_invite = invitation_service.update_invitation_status(event_id, slack_id, RSVP.not_attending)
        result = True if updated_invite is not None else False
    except Exception as e:
        print(e)
        result = False

    response_schema = WithdrawInvitationResponseSchema()
    response = response_schema.load({'success': result})

    BrokerService.respond(response, reply_to, correlation_id)

@MessageHandler.handle('invite_multiple_if_needed')
def invite_multiple_if_needed(payload: dict, correlation_id: str, reply_to: str):
    # Get events in need of invitation
    days_in_advance_to_invite = int(os.environ["DAYS_IN_ADVANCE_TO_INVITE"])
    people_per_event = int(os.environ["PEOPLE_PER_EVENT"])
    events = Event.get_events_in_need_of_invitations(days_in_advance_to_invite, people_per_event)
    events = [{"event_id": event[0], "event_time": event[1].isoformat(), "restaurant_name": event[2], "number_of_already_invited": event[3]} for event in events]

    # Get numbers of users to invite
    events_where_users_were_invited = []
    for event in events:
        number_of_user, users = User.get()
        number_to_invite = people_per_event - event['number_of_already_invited']
        users_to_invite = SlackUser.get_users_to_invite(number_to_invite, event['event_id'], number_of_user, people_per_event)
        user_ids_to_invite = [user[0] for user in users_to_invite]

        if len(user_ids_to_invite) == 0:
            print("Event %s in need of users, but noone to invite" % event['event_id']) # TODO: needs to be handled
            continue

        event_where_users_were_invited = {
            'event_time': event['event_time'],
            'event_id': event['event_id'],
            'restaurant_name': event['restaurant_name'],
            'invited_users': []
        }
        try:
            for user_id in user_ids_to_invite:
                invitation_schema = InvitationSchema()
                invitation = invitation_schema.load(
                    data={"event_id": event['event_id'], "slack_id": user_id},
                    partial=True
                )
                Invitation.upsert(invitation)
                event_where_users_were_invited['invited_users'].append(user_id)
        except Exception as e:
            print(e)
        events_where_users_were_invited.append(event_where_users_were_invited)

    response_schema = InviteMultipleIfNeededResponseSchema()
    response = response_schema.load({'events': events_where_users_were_invited})

    BrokerService.respond(response, reply_to, correlation_id)
