import json
import jsonschema

from app.services.broker import broker
from rabbitmq_pika_flask.ExchangeType import ExchangeType
from app.services.broker.schemas.Message import message_schema, MessageSchema

from app.services.broker.handlers import MessageHandlers
import app.services.broker.handlers.get

@broker.queue(routing_key='rpc', exchange_type = ExchangeType.DIRECT, props_needed = ["correlation_id", "reply_to"])
def rpc(routing_key, body, correlation_id, reply_to):
    try:
        print(body)
        jsonschema.validate(body, message_schema)
    except (jsonschema.ValidationError, json.JSONDecodeError) as e:
        print(e)
        broker.sync_send(None, reply_to, ExchangeType.DIRECT, 5, "v1.0.0", correlation_id=correlation_id)
        return

    schema = MessageSchema()
    message = schema.load(body)

    MessageHandlers.process_message(message, correlation_id, reply_to)
