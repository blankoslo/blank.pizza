import os

from app.services.broker.temp.RabbitMQ import RabbitMQ

from rabbitmq_pika_flask.ExchangeType import ExchangeType
from app.services.broker.schemas.message import MessageSchema


broker = RabbitMQ()

class BrokerService:
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
        broker.sync_send(message, os.environ["MQ_EVENT_KEY"], ExchangeType.DIRECT, 5, "v1.0.0")
