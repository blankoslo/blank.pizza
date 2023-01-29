from rabbitmq_pika_flask.ExchangeType import ExchangeType

from app.services.broker.handlers import MessageHandlers
from app.services.broker.schemas.GetEventsInNeedOfInvitations import GetEventsInNeedOfInvitationsSchema
from app.services.broker import broker

@MessageHandlers.handle('get_events_in_need_of_invitations')
def get_events_in_need_of_invitations(payload: dict, correlation_id: str, reply_to: str):
    schema = GetEventsInNeedOfInvitationsSchema()
    request = schema.load(payload)
    print(request)
    broker.sync_send("response", reply_to, ExchangeType.DIRECT, 5, "v1.0.0", correlation_id=correlation_id)
