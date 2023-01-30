from marshmallow import fields, Schema
from marshmallow_enum import EnumField
from src.database.rsvp import RSVP

class InvitationUpdate(Schema):
    reminded_at = fields.DateTime()
    rsvp = EnumField(RSVP, by_value=True)

class UpdateInvitationRequestSchema(Schema):
    slack_id = fields.Str(required=True)
    event_id = fields.UUID(required=True)
    update_data = fields.Nested(InvitationUpdate, required=True)

class UpdateInvitationResponseSchema(Schema):
    success = fields.Boolean(required=True)
