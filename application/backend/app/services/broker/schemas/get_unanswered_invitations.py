from marshmallow import fields, Schema
from app.services.broker.schemas.slack_message import SlackMessage

class GetUnansweredInvitationsDataSchema(Schema):
    slack_id = fields.Str(required=True)
    event_id = fields.UUID(required=True)
    invited_at = fields.DateTime(required=True)
    reminded_at = fields.DateTime(required=True)
    slack_message = fields.Nested(SlackMessage)
    team_id = fields.Str(required=True)
    bot_token = fields.Str(required=True)

class GetUnansweredInvitationsResponseSchema(Schema):
    invitations = fields.Nested(GetUnansweredInvitationsDataSchema, many=True)
