from marshmallow_jsonschema import JSONSchema
from marshmallow import fields, Schema

from app.services.broker.schemas.GetEventsInNeedOfInvitations import GetEventsInNeedOfInvitationsRequestSchema
class MessageSchema(Schema):
    type = fields.Str(required=True)
    payload = fields.Nested(
        GetEventsInNeedOfInvitationsRequestSchema,
        allow_none=True, required=False)

message_schema = JSONSchema().dump(MessageSchema())
