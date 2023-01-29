from rabbitmq_pika_flask.ExchangeType import ExchangeType

from app.services.broker import broker
from app.services.broker.handlers import MessageHandlers
from app.services.broker.schemas.GetEventsInNeedOfInvitations import GetEventsInNeedOfInvitationsRequestSchema, GetEventsInNeedOfInvitationsResponseSchema
from app.services.broker.schemas.GetUsers import GetUsersResponseSchema
from app.services.broker.schemas.GetUsersToInvite import GetUsersToInviteRequestSchema, GetUsersToInviteResponseSchema
from app.services.broker.schemas.CreateInvitations import CreateInvitationsRequestSchema, CreateInvitationsResponseSchema

from app.models.event import Event
from app.models.user import User, UserSchema
from app.models.slack_user import SlackUser
from app.models.invitation import Invitation
from app.models.invitation_schema import InvitationSchema

def respond(response, reply_to, correlation_id):
    broker.sync_send(response, reply_to, ExchangeType.DIRECT, 5, "v1.0.0", correlation_id=correlation_id)

@MessageHandlers.handle('get_events_in_need_of_invitations')
def get_events_in_need_of_invitations(payload: dict, correlation_id: str, reply_to: str):
    schema = GetEventsInNeedOfInvitationsRequestSchema()
    request = schema.load(payload)
    days_in_advance_to_invite = request.get('days_in_advance_to_invite')
    people_per_event = request.get('people_per_event')

    events = Event.get_events_in_need_of_invitations(days_in_advance_to_invite, people_per_event)
    events = [{"event_id": event[0], "event_time": event[1].isoformat(), "restaurant_name": event[2], "number_of_already_invited": event[3]} for event in events]

    response_schema = GetEventsInNeedOfInvitationsResponseSchema()
    response = response_schema.load({'events': events})

    respond(response, reply_to, correlation_id)

@MessageHandlers.handle('get_users')
def get_users(payload: dict, correlation_id: str, reply_to: str):
    number_of_user, users = User.get()
    response_schema = GetUsersResponseSchema()
    user_schema = UserSchema()
    response = response_schema.load({'users': [user_schema.dump(user) for user in users]})

    respond(response, reply_to, correlation_id)

@MessageHandlers.handle('get_users_to_invite')
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

    respond(response, reply_to, correlation_id)

@MessageHandlers.handle('create_invitations')
def create_invitations(payload: dict, correlation_id: str, reply_to: str):
    schema = CreateInvitationsRequestSchema()
    request = schema.load(payload)
    user_ids = request.get('user_ids')
    event_id = request.get('event_id')

    result = True
    try:
        for user_id in user_ids:
            invitation_schema = InvitationSchema()
            invitation = invitation_schema.load(
                data={"event_id": event_id, "slack_id": user_id},
                partial=True
            )
            Invitation.upsert(invitation)
    except Exception as e:
        print(e)
        result = False

    response_schema = CreateInvitationsResponseSchema()
    response = response_schema.load({'success': result})

    respond(response, reply_to, correlation_id)
