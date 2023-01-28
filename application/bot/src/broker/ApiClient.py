import uuid
import json

from src.broker.AmqpConnection import AmqpConnection
from src.broker.schemas.MessageRequest import MessageRequestSchema

class ApiClient:
    def __init__(self):
        self.mq = AmqpConnection()
        self.mq.connect()
        self.mq.setup_exchange()

        result = self.mq.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.mq.channel.queue_bind(self.callback_queue, exchange=self.mq.exchange)

    def call(self, payload):
        response = None
        corr_id = str(uuid.uuid4())

        def on_response(ch, method, props, body):
            if corr_id == props.correlation_id:
                nonlocal response
                response = body

        self.mq.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=on_response,
            auto_ack=True)

        self.mq.publish_rpc("rpc", self.callback_queue, corr_id, json.dumps(payload))
        self.mq.connection.process_data_events(time_limit=30)
        if response is not None:
            response = response.decode('utf8')
        return response

    def get_events_in_need_of_invitations(self):
        request_data = { "type": "get_events_in_need_of_invitations" }
        request_schema = MessageRequestSchema()
        request = request_schema.load(request_data)
        return self.call(request)


