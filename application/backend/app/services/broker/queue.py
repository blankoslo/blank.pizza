import json
import os
import logging

from marshmallow import ValidationError

from app.services.injector import injector
from app.services.broker import broker
from rabbitmq_pika_flask.ExchangeType import ExchangeType
from app.services.broker.schemas.message import MessageSchema

from app.services.broker.handlers.message_handler import MessageHandler

@broker.queue(routing_key = os.environ["MQ_RPC_KEY"], exchange_type = ExchangeType.DIRECT, props_needed = ["correlation_id", "reply_to"])
def rpc(routing_key, body, correlation_id, reply_to):
    logger = injector.get(logging.Logger)
    try:
        schema = MessageSchema()
        message = schema.load(body)
        logger.info("Got message on %s, with type %s", routing_key, message['type'])

        MessageHandler.process_message(message, correlation_id, reply_to)
    except (ValidationError, json.JSONDecodeError) as e:
        logger.error(e)
        broker.sync_send(None, reply_to, ExchangeType.DIRECT, 5, "v1.0.0", correlation_id=correlation_id)
