import json
import os
from marshmallow import ValidationError

from app.services.broker import broker
from rabbitmq_pika_flask.ExchangeType import ExchangeType
from app.services.broker.schemas.Message import MessageSchema

from app.services.broker.handlers import MessageHandler

@broker.queue(routing_key = os.environ["MQ_RPC_KEY"], exchange_type = ExchangeType.DIRECT, props_needed = ["correlation_id", "reply_to"])
def rpc(routing_key, body, correlation_id, reply_to):
    try:
        schema = MessageSchema()
        message = schema.load(body)

        MessageHandler.process_message(message, correlation_id, reply_to)
    except (ValidationError, json.JSONDecodeError) as e:
        print(e)
        broker.sync_send(None, reply_to, ExchangeType.DIRECT, 5, "v1.0.0", correlation_id=correlation_id)
