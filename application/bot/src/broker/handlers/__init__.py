from src.broker.schemas.Message import MessageSchema
import time
import json

class MessageHandler:
    handlers = {}

    @classmethod
    def handle(cls, type_: str):
        def decorator(func):
            cls.handlers[type_] = func
            return func
        return decorator

    @classmethod
    def process_message(cls, message: dict):
        type_ = message['type']
        payload = message.get('payload')
        cls.handlers[type_](payload)

def on_message(channel, method, properties, body):
    msg = body.decode('utf8')
    schema = MessageSchema()
    message = schema.load(json.loads(msg))

    MessageHandler.process_message(message)

# DO NOT REMOVE: Import handlers to initialize them
# ALSO DO NOT MOVE: having it at the bottom stops circular imports
import src.broker.handlers.finalization
import src.broker.handlers.user_withdrew_after_finalization

