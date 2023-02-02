from rabbitmq_pika_flask.ExchangeType import ExchangeType

from app.services.broker import broker
from app.services.broker.schemas.Message import MessageSchema

class MessageHandler:
    handlers = {}

    @classmethod
    def handle(cls, type_: str):
        def decorator(func):
            cls.handlers[type_] = func
            return func
        return decorator

    @classmethod
    def process_message(cls, message: dict, correlation_id: str, reply_to: str):
        type_ = message['type']
        payload = message.get('payload')
        cls.handlers[type_](payload, correlation_id, reply_to)

    @classmethod
    def respond(cls, response, reply_to, correlation_id):
        broker.sync_send(response, reply_to, ExchangeType.DIRECT, 5, "v1.0.0", correlation_id=correlation_id)

    @classmethod
    def publish(cls, type, response):
        message_schema = MessageSchema()
        message = message_schema.load({
            'type': type,
            'payload': response
        })
        # TODO get queue/routin_key from env variable or something
        broker.sync_send(message, "pizza", ExchangeType.DIRECT, 5, "v1.0.0")

# DO NOT REMOVE: Import handlers to initialize them
# ALSO DO NOT MOVE: having it at the bottom stops circular imports
import app.services.broker.handlers.get
import app.services.broker.handlers.update
import app.services.broker.handlers.create
import app.services.broker.handlers.action
