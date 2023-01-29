from marshmallow import fields, Schema

from src.broker.schemas.GetEventsInNeedOfInvitations import GetEventsInNeedOfInvitationsSchema
from src.broker.schemas.GetUsersToInvite import GetUsersToInviteRequestSchema

class MessageRequestSchema(Schema):
    type = fields.Str(required=True)
    payload = fields.Raw(allow_none=True, required=False)
