import uuid
import json
import os
import logging
import time

from marshmallow import Schema

from src.injector import injector, inject
from src.broker.amqp_connection import AmqpConnection
from src.broker.schemas.message import MessageSchema
from src.broker.schemas.invite_multiple_if_needed import InviteMultipleIfNeededResponseSchema
from src.broker.schemas.get_unanswered_invitations import GetUnansweredInvitationsResponseSchema
from src.broker.schemas.update_invitation import UpdateInvitationRequestSchema, UpdateInvitationResponseSchema
from src.broker.schemas.get_invited_unanswered_user_ids import GetInvitedUnansweredUserIdsResponseSchema
from src.broker.schemas.update_slack_user import UpdateSlackUserRequestSchema, UpdateSlackUserResponseSchema
from src.broker.schemas.create_image import CreateImageRequestSchema, CreateImageResponseSchema
from src.broker.schemas.withdraw_invitation import WithdrawInvitationRequestSchema, WithdrawInvitationResponseSchema
from src.broker.schemas.get_slack_installation import GetSlackInstallationRequestSchema, GetSlackInstallationResponseSchema

class BrokerClient:
    messages = {}

    @inject
    def __init__(self, amqp_connection: AmqpConnection, logger: logging.Logger):
        self.logger = logger
        self.mq = amqp_connection
        self.rpc_key = os.environ["MQ_RPC_KEY"]
        self.timeout = 30
        self.mq.connect()
        self.mq.setup_exchange()

        result = self.mq.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.mq.channel.queue_bind(self.callback_queue, exchange=self.mq.exchange)

    def disconnect(self):
        self.mq.disconnect()

    def on_response(self, ch, method, props, body):
        self.messages[props.correlation_id] = body

    def _call(self, payload):
        response = None
        corr_id = str(uuid.uuid4())

        self.mq.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.mq.publish_rpc(self.rpc_key, self.callback_queue, corr_id, json.dumps(payload, default=str))

        start = time.time()
        while corr_id not in self.messages:
            if time.time() - start >= self.timeout:
                break

            self.mq.connection.process_data_events(time_limit=0.1)

        if corr_id in self.messages:
            response = json.loads(self.messages.pop(corr_id).decode('utf8'))
        else:
            self.logger.warn("Failed to get response from backend")
        return response

    def _create_request(self, type: str, payload: Schema = None):
        request_data = {
            "type": type
        }
        if payload is not None:
            request_data['payload'] = payload
        request_schema = MessageSchema()
        request = request_schema.load(request_data)
        return request

    def get_slack_installation(self, team_id: str):
        request_payload = {
            "team_id": team_id,
        }
        request_payload_schema = GetSlackInstallationRequestSchema()
        response_payload = self._call(self._create_request("get_slack_installation", request_payload_schema.load(request_payload)))
        if response_payload is None:
            return None
        response_schema = GetSlackInstallationResponseSchema()
        response = response_schema.load(response_payload)
        return response

    def invite_multiple_if_needed(self):
        response_payload = self._call(self._create_request("invite_multiple_if_needed"))
        if response_payload is None:
            return []
        response_schema = InviteMultipleIfNeededResponseSchema()
        response = response_schema.load(response_payload)
        return response['events']

    def get_unanswered_invitations(self):
        response_payload = self._call(self._create_request("get_unanswered_invitations"))
        if response_payload is None:
            return []
        response_schema = GetUnansweredInvitationsResponseSchema()
        response = response_schema.load(response_payload)
        return response['invitations']

    def get_unanswered_invitations_on_finished_events_and_set_not_attending(self):
        response_payload = self._call(self._create_request("get_unanswered_invitations_on_finished_events_and_set_not_attending"))
        if response_payload is None:
            return []
        response_schema = GetUnansweredInvitationsResponseSchema()
        response = response_schema.load(response_payload)
        return response['invitations']

    def update_invitation(self, slack_id: str, event_id: str, update_values: dict):
        request_payload = {
            "slack_id": slack_id,
            "event_id": event_id,
            "update_data": update_values
        }
        request_payload_schema = UpdateInvitationRequestSchema()
        response_payload = self._call(self._create_request("update_invitation", request_payload_schema.load(request_payload)))
        if response_payload is None:
            return False
        response_schema = UpdateInvitationResponseSchema()
        response = response_schema.load(response_payload)
        return response['success']

    def get_invited_unanswered_user_ids(self):
        response_payload = self._call(self._create_request("get_invited_unanswered_user_ids"))
        if response_payload is None:
            return []
        response_schema = GetInvitedUnansweredUserIdsResponseSchema()
        response = response_schema.load(response_payload)
        return response['user_ids']

    def  update_slack_user(self, slack_users):
        request_payload = {
            'users_to_update': []
        }
        for slack_user in slack_users:
            slack_id = slack_user['id']
            current_username = slack_user['name']
            email = slack_user['profile']['email']

            request_payload['users_to_update'].append({
                'slack_id': slack_id,
                'current_username': current_username,
                'email': email,
            })
        request_payload_schema = UpdateSlackUserRequestSchema()
        response_payload = self._call(self._create_request("update_slack_user", request_payload_schema.load(request_payload)))
        response_schema = UpdateSlackUserResponseSchema()
        if response_payload is None:
            return response_schema.load({
                'success': False,
                'updated_users': [],
                'failed_users': [user['slack_id'] for user in request_payload['users_to_update']]
            })
        response = response_schema.load(response_payload)
        return response

    def create_image(self, cloudinary_id, slack_id, title):
        request_payload = {
            "cloudinary_id": cloudinary_id,
            "slack_id": slack_id,
            'title': title
        }
        request_payload_schema = CreateImageRequestSchema()
        response_payload = self._call(self._create_request("create_image", request_payload_schema.load(request_payload)))
        if response_payload is None:
            return False
        response_schema = CreateImageResponseSchema()
        response = response_schema.load(response_payload)
        return response['success']

    def withdraw_invitation(self, event_id, slack_id):
        request_payload = {
            "slack_id": slack_id,
            'event_id': event_id
        }
        request_payload_schema = WithdrawInvitationRequestSchema()
        response_payload = self._call(self._create_request("withdraw_invitation", request_payload_schema.load(request_payload)))
        if response_payload is None:
            return False
        response_schema = WithdrawInvitationResponseSchema()
        response = response_schema.load(response_payload)
        return response['success']
