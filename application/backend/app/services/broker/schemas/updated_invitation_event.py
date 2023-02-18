from marshmallow import fields, Schema
from app.models.enums import RSVP
from marshmallow_enum import EnumField

from app.services.broker.schemas.slack_message import SlackMessage

class UpdatedInvitationEventSchema(Schema):
    event_id = fields.UUID(required=True)
    slack_id = fields.Str(required=True)
    rsvp = EnumField(RSVP, by_value=True, required=True)
    slack_message = fields.Nested(SlackMessage)
