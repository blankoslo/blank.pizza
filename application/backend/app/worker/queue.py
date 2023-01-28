from app.services.broker import broker
from rabbitmq_pika_flask.ExchangeType import ExchangeType

@broker.queue(routing_key='rpc', exchange_type = ExchangeType.DIRECT, props_needed = ["message_id"])
def ping_event(routing_key, body, message_id, *args, **kwarfs):
    print(body)
    print(routing_key)
    print(args)
    print(kwarfs)
    print(message_id)
    '''ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))'''
