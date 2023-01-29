from rabbitmq_pika_flask.ExchangeType import ExchangeType

from app.services.broker.handlers import MessageHandlers
from app.services.broker.schemas.GetEventsInNeedOfInvitations import GetEventsInNeedOfInvitationsRequestSchema, GetEventsInNeedOfInvitationsResponseSchema
from app.services.broker.schemas.GetUsers import GetUsersResponseSchema
from app.services.broker import broker

from app.models.event import Event
from app.models.user import User, UserSchema

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
