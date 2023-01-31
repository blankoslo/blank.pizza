from app.services.broker.handlers import MessageHandler

from app.services.broker.schemas.GetEventsInNeedOfInvitations import GetEventsInNeedOfInvitationsRequestSchema, GetEventsInNeedOfInvitationsResponseSchema
from app.services.broker.schemas.GetUsers import GetUsersResponseSchema
from app.services.broker.schemas.GetUsersToInvite import GetUsersToInviteRequestSchema, GetUsersToInviteResponseSchema
from app.services.broker.schemas.GetUnansweredInvitations import GetUnansweredInvitationsResponseSchema, GetUnansweredInvitationsDataSchema

from app.models.event import Event
from app.models.user import User, UserSchema
from app.models.slack_user import SlackUser
from app.models.invitation import Invitation
from app.models.enums import RSVP

@MessageHandler.handle('get_events_in_need_of_invitations')
def get_events_in_need_of_invitations(payload: dict, correlation_id: str, reply_to: str):
    schema = GetEventsInNeedOfInvitationsRequestSchema()
    request = schema.load(payload)
    days_in_advance_to_invite = request.get('days_in_advance_to_invite')
    people_per_event = request.get('people_per_event')

    events = Event.get_events_in_need_of_invitations(days_in_advance_to_invite, people_per_event)
    events = [{"event_id": event[0], "event_time": event[1].isoformat(), "restaurant_name": event[2], "number_of_already_invited": event[3]} for event in events]

    response_schema = GetEventsInNeedOfInvitationsResponseSchema()
    response = response_schema.load({'events': events})

    MessageHandler.respond(response, reply_to, correlation_id)

@MessageHandler.handle('get_users')
def get_users(payload: dict, correlation_id: str, reply_to: str):
    number_of_user, users = User.get()
    response_schema = GetUsersResponseSchema()
    user_schema = UserSchema()
    response = response_schema.load({'users': [user_schema.dump(user) for user in users]})

    MessageHandler.respond(response, reply_to, correlation_id)

@MessageHandler.handle('get_users_to_invite')
def get_users_to_invite(payload: dict, correlation_id: str, reply_to: str):
    schema = GetUsersToInviteRequestSchema()
    request = schema.load(payload)
    number_of_users_to_invite = request.get('number_of_users_to_invite')
    event_id = request.get('event_id')
    total_number_of_employees = request.get('total_number_of_employees')
    employees_per_event = request.get('employees_per_event')

    users = SlackUser.get_users_to_invite(number_of_users_to_invite, event_id, total_number_of_employees, employees_per_event)
    users = [{"id": user[0]} for user in users]

    response_schema = GetUsersToInviteResponseSchema()
    response = response_schema.load({'users': users})

    MessageHandler.respond(response, reply_to, correlation_id)

@MessageHandler.handle('get_unanswered_invitations')
def get_unanswered_invitations(payload: dict, correlation_id: str, reply_to: str):
    invitations = Invitation.get_by_filter({"rsvp": RSVP.unanswered})
    response_schema = GetUnansweredInvitationsResponseSchema()
    response_data = [{"slack_id": invitation.slack_id, "event_id": invitation.event_id, "invited_at": invitation.invited_at.isoformat(), "reminded_at": invitation.reminded_at.isoformat() } for invitation in invitations]
    response = response_schema.load({'invitations': response_data})

    MessageHandler.respond(response, reply_to, correlation_id)
