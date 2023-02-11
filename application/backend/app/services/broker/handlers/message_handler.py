from marshmallow import Schema

from app.services.broker import BrokerService

class MessageHandler:
    handlers = {}

    @classmethod
    def handle(cls, type_: str, incoming_schema: Schema = None, outgoing_schema: Schema = None):
        def decorator(func):
            cls.handlers[type_] = {
            'func': func,
            'incoming_schema': incoming_schema,
            'outgoing_schema': outgoing_schema
            }
            return func
        return decorator

    @classmethod
    def process_message(cls, message: dict, correlation_id: str, reply_to: str):
        type_ = message['type']
        handler = cls.handlers[type_]
        if handler['incoming_schema'] is not None:
            schema = handler['incoming_schema']()
            payload = schema.load(message.get('payload'))
            response = handler['func'](payload)
        else:
            response = handler['func']()

        if handler['outgoing_schema'] is not None:
            schema = handler['outgoing_schema']()
            response = schema.load(response)
        BrokerService.respond(response, reply_to, correlation_id)
