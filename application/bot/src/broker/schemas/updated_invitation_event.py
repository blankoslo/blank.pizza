from marshmallow import fields, Schema
from marshmallow_enum import EnumField
from src.rsvp import RSVP

from src.broker.schemas.slack_message import SlackMessage

class UpdatedInvitationEventSchema(Schema):
    event_id = fields.UUID(required=True)
    slack_id = fields.Str(required=True)
    rsvp = EnumField(RSVP, by_value=True, required=True)
    slack_message = fields.Nested(SlackMessage)
    team_id = fields.Str(required=True)
    bot_token = fields.Str(required=True)
