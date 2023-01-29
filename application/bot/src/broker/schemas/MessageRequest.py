from marshmallow import fields, Schema

from src.broker.schemas.GetEventsInNeedOfInvitations import GetEventsInNeedOfInvitationsSchema

class MessageRequestSchema(Schema):
    type = fields.Str(required=True)
    payload = fields.Nested(
        GetEventsInNeedOfInvitationsSchema,
        allow_none=True)
