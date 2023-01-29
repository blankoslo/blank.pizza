import uuid
import json

from marshmallow import Schema

from src.broker.AmqpConnection import AmqpConnection
from src.broker.schemas.GetEventsInNeedOfInvitations import GetEventsInNeedOfInvitationsSchema, GetEventsInNeedOfInvitationsResponseSchema
from src.broker.schemas.MessageRequest import MessageRequestSchema

class ApiClient:
    def __init__(self):
        self.mq = AmqpConnection()
        self.mq.connect()
        self.mq.setup_exchange()

        result = self.mq.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.mq.channel.queue_bind(self.callback_queue, exchange=self.mq.exchange)

    def _call(self, payload):
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
            response = json.loads(response.decode('utf8'))
        return response

    def _create_request(self, type: str, payload: Schema):
        request_data = {
            "type": type,
            "payload": payload
        }
        request_schema = MessageRequestSchema()
        request = request_schema.load(request_data)
        return request

    def get_events_in_need_of_invitations(self, days_in_advance_to_invite: int, people_per_event: int):
        request_payload = {
            "days_in_advance_to_invite": days_in_advance_to_invite,
            "people_per_event": people_per_event
        }
        request_payload_schema = GetEventsInNeedOfInvitationsSchema()
        response_payload = self._call(self._create_request("get_events_in_need_of_invitations", request_payload_schema.load(request_payload)))
        if response_payload is None:
            return None
        response_schema = GetEventsInNeedOfInvitationsResponseSchema()
        response = response_schema.load(response_payload)
        print(response['events'])
        return response['events']


