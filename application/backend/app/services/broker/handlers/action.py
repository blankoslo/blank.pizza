from datetime import datetime
import os
import logging

from app.services.broker.handlers.message_handler import MessageHandler

from app.services.broker.schemas.withdraw_invitation import WithdrawInvitationRequestSchema, WithdrawInvitationResponseSchema
from app.services.broker.schemas.invite_multiple_if_needed import InviteMultipleIfNeededResponseSchema

from app.models.enums import RSVP
from app.services.injector import injector
from app.services.invitation_service import InvitationService
from app.services.slack_user_service import SlackUserService
from app.services.event_service import EventService

@MessageHandler.handle('withdraw_invitation', WithdrawInvitationRequestSchema, WithdrawInvitationResponseSchema)
def withdraw_invitation(request: dict):
    logger = injector.get(logging.Logger)
    invitation_service = injector.get(InvitationService)

    event_id = request.get('event_id')
    slack_id = request.get('slack_id')

    try:
        updated_invite = invitation_service.update_invitation_status(event_id, slack_id, RSVP.not_attending)
        result = True if updated_invite is not None else False
    except Exception as e:
        logger.warning(e)
        result = False

    return {'success': result}

@MessageHandler.handle('invite_multiple_if_needed', outgoing_schema = InviteMultipleIfNeededResponseSchema)
def invite_multiple_if_needed():
    logger = injector.get(logging.Logger)
    invitation_service = injector.get(InvitationService)
    slack_user_service = injector.get(SlackUserService)
    event_service = injector.get(EventService)
    # Get events in need of invitation
    people_per_event = int(os.environ["PEOPLE_PER_EVENT"])
    events = event_service.get_events_in_need_of_invitations()
    events = [{
        "event_id": event[0],
        "event_time": event[1].isoformat(),
        "restaurant_name": event[2],
        "team_id": event[3],
        "bot_token": event[4],
        "number_of_already_invited": event[5]
    } for event in events]

    # Get numbers of users to invite
    events_where_users_were_invited = []
    for event in events:
        number_of_user, users = slack_user_service.get()
        number_to_invite = people_per_event - event['number_of_already_invited']
        user_ids_to_invite = slack_user_service.get_user_ids_to_invite(number_to_invite, event['event_id'], number_of_user, people_per_event)

        if len(user_ids_to_invite) == 0:
            logger.warning("Event %s in need of users, but noone to invite" % event['event_id']) # TODO: needs to be handled
            continue

        event_where_users_were_invited = {
            'event_time': event['event_time'],
            'event_id': event['event_id'],
            'restaurant_name': event['restaurant_name'],
            'team_id': event['team_id'],
            'bot_token': event['bot_token'],
            'invited_users': []
        }
        try:
            for user_id in user_ids_to_invite:
                invitation_service.add(event['event_id'], user_id)
                event_where_users_were_invited['invited_users'].append(user_id)
        except Exception as e:
            logger.error(e)
        events_where_users_were_invited.append(event_where_users_were_invited)

    return {'events': events_where_users_were_invited}
