from app.services.broker import broker
from rabbitmq_pika_flask.ExchangeType import ExchangeType

@broker.queue(routing_key='rpc', exchange_type = ExchangeType.DIRECT, props_needed = ["correlation_id", "reply_to"])
def ping_event(routing_key, body, correlation_id, reply_to):
    broker.sync_send("response", reply_to, ExchangeType.DIRECT, 5, "v1.0.0", correlation_id=correlation_id)
