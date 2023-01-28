from app.services.broker import broker
from rabbitmq_pika_flask.ExchangeType import ExchangeType

@broker.queue(routing_key='rpc', exchange_type = ExchangeType.DIRECT, props_needed = ["correlation_id", "reply_to"])
def ping_event(routing_key, body, correlation_id, reply_to):
    print(body)
    print(routing_key)
    print(correlation_id)
    print(reply_to)
    print("replying")
    broker.sync_send("response", reply_to, ExchangeType.DIRECT, 5, "v1.0.0", correlation_id=correlation_id)
    print("replied")
    '''ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))'''
