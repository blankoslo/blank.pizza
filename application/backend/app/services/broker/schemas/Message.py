from marshmallow_jsonschema import JSONSchema
from marshmallow import fields, Schema

from app.services.broker.schemas.GetEventsInNeedOfInvitations import GetEventsInNeedOfInvitationsSchema
class MessageSchema(Schema):
    type = fields.Str(required=True)
    payload = fields.Nested(
        GetEventsInNeedOfInvitationsSchema,
        allow_none=True)

message_schema = JSONSchema().dump(MessageSchema())
