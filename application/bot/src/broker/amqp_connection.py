import pika
import functools
import os
from retry import retry
import logging
from src.broker.amqp_connection_pool import AmqpConnectionPool

class AmqpConnection:
    def __init__(self, logger: logging.Logger, connection_pool: AmqpConnectionPool):
        self.exchange = os.environ.get('MQ_EXCHANGE')
        self.queue = os.environ.get('MQ_EVENT_QUEUE')
        self.routing_key = os.environ.get('MQ_EVENT_KEY')
        self.logger = logger
        self.connection_pool = connection_pool
        self.channel = None
        self.connection = None

    def disconnect(self):
        if self.channel is not None and not self.channel.is_closed:
            self.channel.stop_consuming()
        self.connection_pool.release_connection(self.connection)

    def connect(self):
        self.connection = self.connection_pool.get_connection()
        self.channel = self.connection.channel()
        self.channel.add_on_close_callback(self._release_connection)

    def _release_connection(self):
        self.connection_pool.release_connection(self.connection)

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
        else:
            self.logger.warning("Connection is not open or channel is not open")

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
        if self.channel is None or self.channel.is_closed:
            self.connect()
            self.setup_queues()
        try:
            self.channel.basic_consume(queue=self.queue, auto_ack=True, on_message_callback=on_message)
            self.channel.start_consuming()
        except pika.exceptions.ChannelClosedByBroker:
            self.logger.warning('Channel Closed By Broker Exception')
