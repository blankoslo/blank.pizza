import uuid
import json

from marshmallow import Schema

from src.broker.AmqpConnection import AmqpConnection
from src.broker.schemas.GetEventsInNeedOfInvitations import GetEventsInNeedOfInvitationsSchema, GetEventsInNeedOfInvitationsResponseSchema
from src.broker.schemas.Message import MessageSchema
from src.broker.schemas.GetUsers import GetUsersResponseSchema
from src.broker.schemas.GetUsersToInvite import GetUsersToInviteRequestSchema, GetUsersToInviteResponseSchema
from src.broker.schemas.CreateInvitations import CreateInvitationsRequestSchema, CreateInvitationsResponseSchema
from src.broker.schemas.GetUnansweredInvitations import GetUnansweredInvitationsResponseSchema
from src.broker.schemas.UpdateInvitation import UpdateInvitationRequestSchema, UpdateInvitationResponseSchema
from src.broker.schemas.GetInvitedUnansweredUserIds import GetInvitedUnansweredUserIdsResponseSchema
from src.broker.schemas.UpdateSlackUser import UpdateSlackUserRequestSchema, UpdateSlackUserResponseSchema
from src.broker.schemas.CreateImage import CreateImageRequestSchema, CreateImageResponseSchema
from src.broker.schemas.WithdrawInvitation import WithdrawInvitationRequestSchema, WithdrawInvitationResponseSchema

class ApiClient:
    messages = {}

    def __init__(self):
        self.mq = AmqpConnection()
        self.mq.connect()
        self.mq.setup_exchange()

        result = self.mq.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.mq.channel.queue_bind(self.callback_queue, exchange=self.mq.exchange)

    def __del__(self):
        self.mq.__del__()

    def on_response(self, ch, method, props, body):
        self.messages[props.correlation_id] = body

    def _call(self, payload):
        response = None
        corr_id = str(uuid.uuid4())

        self.mq.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.mq.publish_rpc("rpc", self.callback_queue, corr_id, json.dumps(payload, default=str))
        self.mq.connection.process_data_events(time_limit=30)

        if corr_id in self.messages:
            response = json.loads(self.messages[corr_id].decode('utf8'))
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

    def get_events_in_need_of_invitations(self, days_in_advance_to_invite: int, people_per_event: int):
        request_payload = {
            "days_in_advance_to_invite": days_in_advance_to_invite,
            "people_per_event": people_per_event
        }
        request_payload_schema = GetEventsInNeedOfInvitationsSchema()
        response_payload = self._call(self._create_request("get_events_in_need_of_invitations", request_payload_schema.load(request_payload)))
        if response_payload is None:
            return []
        response_schema = GetEventsInNeedOfInvitationsResponseSchema()
        response = response_schema.load(response_payload)
        return response['events']

    def get_users(self):
        response_payload = self._call(self._create_request("get_users"))
        if response_payload is None:
            return []
        response_schema = GetUsersResponseSchema()
        response = response_schema.load(response_payload)
        return response['users']

    def get_users_to_invite(self, number_of_users_to_invite: int, event_id: uuid.UUID, total_number_of_employees: int, employees_per_event: int):
        request_payload = {
            "number_of_users_to_invite": number_of_users_to_invite,
            "event_id": event_id,
            "total_number_of_employees": total_number_of_employees,
            "employees_per_event": employees_per_event
        }
        request_payload_schema = GetUsersToInviteRequestSchema()
        response_payload = self._call(self._create_request("get_users_to_invite", request_payload_schema.load(request_payload)))
        if response_payload is None:
            return []
        response_schema = GetUsersToInviteResponseSchema()
        response = response_schema.load(response_payload)
        return response['users']

    def create_invitations(self, user_ids: [str], event_id: str):
        request_payload = {
            "user_ids": user_ids,
            "event_id": event_id,
        }
        request_payload_schema = CreateInvitationsRequestSchema()
        response_payload = self._call(self._create_request("create_invitations", request_payload_schema.load(request_payload)))
        if response_payload is None:
            return False
        response_schema = CreateInvitationsResponseSchema()
        response = response_schema.load(response_payload)
        return response['success']

    def get_unanswered_invitations(self):
        response_payload = self._call(self._create_request("get_unanswered_invitations"))
        if response_payload is None:
            return []
        response_schema = GetUnansweredInvitationsResponseSchema()
        response = response_schema.load(response_payload)
        return response['invitations']

    def update_invitation(self, slack_id: str, event_id: str, people_per_event: int, update_values: dict):
        request_payload = {
            "slack_id": slack_id,
            "event_id": event_id,
            "people_per_event": people_per_event,
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

    def update_slack_user(self, slack_user):
        slack_id = slack_user['id']
        current_username = slack_user['name']
        email = slack_user['profile']['email']

        request_payload = {
            "slack_id": slack_id,
            "update_data": {
                'current_username': current_username,
                'email': email,
            }
        }
        request_payload_schema = UpdateSlackUserRequestSchema()
        response_payload = self._call(self._create_request("update_slack_user", request_payload_schema.load(request_payload)))
        if response_payload is None:
            return False
        response_schema = UpdateSlackUserResponseSchema()
        response = response_schema.load(response_payload)
        return response['success']

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
