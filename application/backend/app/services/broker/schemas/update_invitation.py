from marshmallow import fields, Schema
from marshmallow_enum import EnumField
from app.models.enums import RSVP
from app.services.broker.schemas.slack_message import SlackMessage

class InvitationUpdate(Schema):
    reminded_at = fields.DateTime()
    rsvp = EnumField(RSVP, by_value=True)
    slack_message = fields.Nested(SlackMessage)

class UpdateInvitationRequestSchema(Schema):
    slack_id = fields.Str(required=True)
    event_id = fields.UUID(required=True)
    update_data = fields.Nested(InvitationUpdate, required=True)

class UpdateInvitationResponseSchema(Schema):
    success = fields.Boolean(required=True)

