from src.broker.AmqpConnection import AmqpConnection
import uuid
import threading
import os
import json

class ApiClient:
    internal_lock = threading.Lock()

    def __init__(self):
        self.mq = AmqpConnection()
        self.mq.connect()
        self.mq.setup_exchange()

        result = self.mq.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        #self.response = None
        #self.corr_id = None

    #def on_response(self, ch, method, props, body):
    #    if self.corr_id == props.correlation_id:
    #        self.response = body

    def call(self, n):
        #self.response = None
        response = None
        corr_id = str(uuid.uuid4())

        def on_response(ch, method, props, body):
            print(body)
            if corr_id == props.correlation_id:
                nonlocal response
                response = body

        print("new queue consume")
        self.mq.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=on_response,
            auto_ack=True)

        #self.corr_id = str(uuid.uuid4())
        #self.mq.publish(self.callback_queue, self.corr_id, str(n))
        print("before publish")
        print(corr_id)
        self.mq.publish_rpc("rpc", self.callback_queue, corr_id, json.dumps(n))
        print("after publish before process")
        self.mq.connection.process_data_events(time_limit=30)
        print("after process")
        return response
