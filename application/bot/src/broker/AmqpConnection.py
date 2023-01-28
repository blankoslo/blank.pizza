import pika
import functools
import os
from retry import retry

class AmqpConnection:
    def __init__(self, host = None, exchange = None):
        self.host = host if host is not None else os.environ.get('MQ_URL')
        self.exchange = exchange if exchange is not None else os.environ.get('MQ_EXCHANGE')
        self.connection = None
        self.channel = None
        self.queue = 'Pizza_Queue'
        self.routing_key = 'pizza'

    def connect(self, connection_name='Neat-App'):
        print('Attempting to connect')
        parameters = pika.URLParameters(self.host)
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()
        print('Connected Successfully')

    def setup_exchange(self):
        self.channel.exchange_declare(self.exchange, exchange_type='direct')

    def setup_queues(self):
        return self.channel.queue_declare(self.queue)

    def setup_binding(self):
        self.channel.queue_bind(self.queue, exchange=self.exchange, routing_key=self.routing_key)

    def do_async(self, callback, *args, **kwargs):
        if self.connection.is_open:
            self.connection.add_callback_threadsafe(functools.partial(callback, *args, **kwargs))

    def publish(self, payload):
        if self.connection.is_open and self.channel.is_open:
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=payload
            )

    def publish_rpc(self, routing_key, reply_to, correlation_id, payload):
        if self.connection.is_open and self.channel.is_open:
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=routing_key,
                properties=pika.BasicProperties(
                    reply_to=reply_to,
                    correlation_id=correlation_id,
                ),
                body=payload
            )
            print("published")
        else:
            print("Connection is not open or channel is not open")

    @retry(pika.exceptions.AMQPConnectionError, delay=1, backoff=2)
    def consume(self, on_message):
        if self.connection.is_closed or self.channel.is_closed:
            self.connect()
            self.setup_queues()
        try:
            self.channel.basic_consume(queue=self.queue, auto_ack=True, on_message_callback=on_message)
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print('Keyboard interrupt received')
            self.channel.stop_consuming()
            self.connection.close()
            os._exit(1)
        except pika.exceptions.ChannelClosedByBroker:
            print('Channel Closed By Broker Exception')
