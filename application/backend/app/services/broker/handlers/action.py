from datetime import datetime
import pytz
import os

from app.services.broker.handlers import MessageHandler

from app.services.broker.schemas.FinalizationEventEvent import FinalizationEventEventSchema
from app.services.broker.schemas.WithdrawInvitation import WithdrawInvitationRequestSchema, WithdrawInvitationResponseSchema
from app.services.broker.schemas.UserWithdrewAfterFinalizationEvent import UserWithdrewAfterFinalizationEventSchema
from app.services.broker.schemas.InviteMultipleIfNeeded import InviteMultipleIfNeededResponseSchema

from app.models.event import Event
from app.models.user import User
from app.models.slack_user import SlackUser
from app.models.event_schema import EventSchema
from app.models.invitation import Invitation
from app.models.invitation_schema import InvitationSchema
from app.models.enums import RSVP
from app.models.restaurant import Restaurant

@MessageHandler.handle('withdraw_invitation')
def withdraw_invitation(payload: dict, correlation_id: str, reply_to: str):
    schema = WithdrawInvitationRequestSchema()
    request = schema.load(payload)
    event_id = request.get('event_id')
    slack_id = request.get('slack_id')

    #Check if event is in past
    result = True
    try:
        event = Event.get_by_id(event_id)
        if event.time < datetime.now(pytz.utc):
            result = False
        else:
            # Update invitation to not attending
            invitation = Invitation.get_by_id(event_id, slack_id)
            update_data = {
                'rsvp': RSVP.not_attending
            }
            updated_invitation = InvitationSchema().load(data=update_data, instance=invitation, partial=True)
            Invitation.upsert(updated_invitation)
            if event.finalized:
                restaurant = Restaurant.get_by_id(event.restaurant_id)
                attending_users = [user[0] for user in Invitation.get_attending_users(event.id)]
                # Publish event that user withdrew after finalization
                queue_event_schema = UserWithdrewAfterFinalizationEventSchema()
                queue_event = queue_event_schema.load({
                    'event_id': event.id,
                    'slack_id': slack_id,
                    'timestamp': event.time.isoformat(),
                    'restaurant_name': restaurant.name
                })
                MessageHandler.publish("user_withdrew_after_finalization", queue_event)
                # Mark event as unfinalized
                update_data = {
                    'finalized': False
                }
                updated_invitation = EventSchema().load(data=update_data, instance=event, partial=True)
                Event.upsert(updated_invitation)
                # Publish event that event is unfinalized
                queue_event_schema = FinalizationEventEventSchema()
                queue_event = queue_event_schema.load({
                    'is_finalized': False,
                    'event_id': event.id,
                    'timestamp': event.time.isoformat(),
                    'restaurant_name': restaurant.name,
                    'slack_ids': attending_users
                })
                MessageHandler.publish("finalization", queue_event)
    except Exception as e:
        print(e)
        result = False

    response_schema = WithdrawInvitationResponseSchema()
    response = response_schema.load({'success': result})

    MessageHandler.respond(response, reply_to, correlation_id)

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

    MessageHandler.respond(response, reply_to, correlation_id)
