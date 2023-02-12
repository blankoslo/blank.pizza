import pika
import functools
import os
from retry import retry
import logging
from src.injector import injector

class AmqpConnection:
    def __init__(self, host = None, exchange = None):
        # CLOUDAMQP_URL is the environment variable created by heroku during production deployment
        mq_url = os.environ.get('MQ_URL') if 'MQ_URL' in os.environ else os.environ.get('CLOUDAMQP_URL')
        self.host = host if host is not None else mq_url
        self.exchange = exchange if exchange is not None else os.environ.get('MQ_EXCHANGE')
        self.connection = None
        self.channel = None
        self.queue = os.environ.get('MQ_EVENT_QUEUE')
        self.routing_key = os.environ.get('MQ_EVENT_KEY')
        self.logger = injector.get(logging.Logger)

    def disconnect(self):
        if self.channel is not None and not self.channel.is_closed:
            self.channel.stop_consuming()
        if self.connection is not None and not self.connection.is_closed:
            self.connection.close()

    def connect(self):
        parameters = pika.URLParameters(self.host)
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()

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
        else:
            self.logger.warning("Connection is not open or channel is not open")

    @retry(pika.exceptions.AMQPConnectionError, delay=1, backoff=2)
    def consume(self, on_message):
        if self.connection.is_closed or self.channel.is_closed:
            self.connect()
            self.setup_queues()
        try:
            self.channel.basic_consume(queue=self.queue, auto_ack=True, on_message_callback=on_message)
            self.channel.start_consuming()
        except pika.exceptions.ChannelClosedByBroker:
            self.logger.warning('Channel Closed By Broker Exception')
